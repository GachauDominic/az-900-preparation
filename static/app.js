/* Progressive enhancement only: the site works without JavaScript, except for
   progress tracking, instant feedback and the exam timer. */
(function () {
  "use strict";
  var KEY = "az900.progress.v1";

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || { modules: {}, exam: null, last: null }; }
    catch (e) { return { modules: {}, exam: null, last: null }; }
  }
  function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) { /* storage unavailable */ } }

  var progress = load();

  /* ---- home: progress bars and "continue" ---------------------------- */
  document.querySelectorAll("[data-module-card]").forEach(function (row) {
    var id = row.getAttribute("data-module-card");
    var m = progress.modules[id];
    var bar = row.querySelector("[data-progress]");
    var label = row.querySelector("[data-status]");
    if (!bar || !label) return;
    if (m && typeof m.best === "number") {
      bar.value = m.best;
      label.textContent = "Best quiz score " + m.best + "%";
    } else if (m && m.read) {
      label.textContent = "Notes read";
    }
  });
  var cont = document.querySelector("[data-continue]");
  if (cont && progress.last) {
    var link = document.createElement("a");
    link.href = progress.last.url;
    link.textContent = progress.last.title;
    cont.textContent = "Continue where you left off: ";
    cont.appendChild(link);
    cont.hidden = false;
  }

  /* ---- module page: mark as read -------------------------------------- */
  var notes = document.querySelector(".notes[data-module]");
  if (notes) {
    var mid = notes.getAttribute("data-module");
    var btn = document.querySelector("[data-mark-read]");
    var title = (notes.querySelector("h1") || {}).textContent || mid;
    progress.last = { url: location.pathname, title: title };
    save(progress);
    var paint = function () {
      var read = !!(progress.modules[mid] && progress.modules[mid].read);
      btn.setAttribute("aria-pressed", read ? "true" : "false");
      btn.textContent = read ? "Notes marked as read" : "Mark notes as read";
    };
    if (btn) {
      paint();
      btn.addEventListener("click", function () {
        var m = progress.modules[mid] || (progress.modules[mid] = {});
        m.read = !m.read;
        save(progress);
        paint();
      });
    }
    /* copy buttons on code blocks */
    notes.querySelectorAll("pre").forEach(function (pre) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "copy-btn";
      b.textContent = "Copy";
      b.addEventListener("click", function () {
        var text = pre.querySelector("code") ? pre.querySelector("code").textContent : pre.textContent;
        if (navigator.clipboard) {
          navigator.clipboard.writeText(text).then(function () {
            b.textContent = "Copied";
            setTimeout(function () { b.textContent = "Copy"; }, 1500);
          });
        }
      });
      pre.appendChild(b);
    });
  }

  /* ---- results: remember best score ----------------------------------- */
  var result = document.querySelector("[data-result]");
  if (result) {
    var pct = parseInt(result.getAttribute("data-percent"), 10);
    var kind = result.getAttribute("data-kind");
    var key = result.getAttribute("data-key");
    var now = new Date().toISOString();
    if (kind === "module") {
      var m = progress.modules[key] || (progress.modules[key] = {});
      if (typeof m.best !== "number" || pct > m.best) m.best = pct;
      m.last = now;
    } else if (kind === "exam") {
      progress.exam = { best: Math.max(pct, (progress.exam && progress.exam.best) || 0), last: now };
    }
    save(progress);
  }

  /* ---- reset ------------------------------------------------------------ */
  var reset = document.querySelector("[data-reset]");
  if (reset) {
    reset.addEventListener("click", function () {
      if (confirm("Clear your saved progress in this browser?")) {
        try { localStorage.removeItem(KEY); } catch (e) { /* ignore */ }
        location.reload();
      }
    });
  }

  /* ---- practice mode: instant feedback ---------------------------------- */
  var form = document.querySelector("[data-quiz-form]");
  if (form && form.getAttribute("data-mode") === "practice") {
    form.querySelectorAll(".question").forEach(function (fs) {
      var btn = fs.querySelector("[data-check]");
      var box = fs.querySelector("[data-feedback]");
      if (!btn || !box) return;
      btn.hidden = false;
      btn.addEventListener("click", function () {
        var qid = fs.getAttribute("data-qid");
        var type = fs.getAttribute("data-type");
        var answer;
        if (type === "yesno") {
          answer = {};
          fs.querySelectorAll("input[type=radio]:checked").forEach(function (r) {
            answer[r.name.split(".").pop()] = r.value === "yes";
          });
        } else {
          answer = [];
          fs.querySelectorAll("input:checked").forEach(function (i) { answer.push(i.value); });
        }
        fetch("/api/check", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question_id: qid, answer: answer })
        }).then(function (r) { return r.json(); }).then(function (d) {
          if (d.error) { box.textContent = d.error; return; }
          box.className = "feedback " + (d.correct ? "good" : "bad");
          box.textContent = "";
          var head = document.createElement("strong");
          head.className = d.correct ? "good" : "bad";
          head.textContent = d.correct ? "Correct. " : (d.answered ? "Not quite. " : "Choose an answer first. ");
          box.appendChild(head);
          var p = document.createElement("span");
          p.textContent = d.explanation;
          box.appendChild(p);
          if (!d.correct && d.answered) {
            var ul = document.createElement("ul");
            d.rows.forEach(function (row) {
              var li = document.createElement("li");
              if (d.type === "yesno") {
                li.textContent = row.text + " Correct answer: " + row.expected + (row.note ? ". " + row.note : "");
              } else if (row.selected && !row.is_correct) {
                li.textContent = "You chose: " + row.text + (row.note ? " " + row.note : "");
              } else { return; }
              ul.appendChild(li);
            });
            if (ul.children.length) box.appendChild(ul);
          }
        }).catch(function () { box.textContent = "Could not check this answer. Try again."; });
      });
    });
  }

  /* ---- exam timer --------------------------------------------------------- */
  var timer = document.querySelector("[data-timer-minutes]");
  if (timer && form) {
    var end = Date.now() + parseInt(timer.getAttribute("data-timer-minutes"), 10) * 60000;
    var out = timer.querySelector("[data-timer-display]");
    var tick = function () {
      var left = Math.max(0, Math.round((end - Date.now()) / 1000));
      var mm = Math.floor(left / 60), ss = left % 60;
      out.textContent = mm + ":" + (ss < 10 ? "0" : "") + ss;
      if (left <= 300) timer.classList.add("low");
      if (left === 0) { clearInterval(iv); form.submit(); }
    };
    var iv = setInterval(tick, 1000);
    tick();
  }
})();
