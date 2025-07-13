document.addEventListener("DOMContentLoaded", function () {
  const timelineContainer = document.getElementById("timeline");
  const modal = document.getElementById("companyModal");
  const modalBody = document.getElementById("modalBody");
  const closeModalBtn = document.querySelector(".close-modal");

  const experiences = [
    {
      company: "CertifyOS",
      date: "Sep 2024 – Present",
      title: "Senior Data Engineer / Lead",
      // description:
      //   "Led the CB1.5 pipeline — a config-driven data ingestion system handling 500+ file variations. Developed a fuzzy Matching Engine to improve attribution accuracy to 97%. Implemented NCQA License Refresh automation and served as de facto Data Engineering Lead.",
      type: "type1",
      icon: "💼",
      link: "companies/certifyos.html"
    },
    {
      company: "6sense",
      date: "Oct 2022 – Sep 2024",
      title: "Senior Data Engineer",
      // description:
      //   "Architected the Singlestore ETL Framework, enabling real-time + batch ingestion across Trino, Hive, and S3. Built internal tooling including a Data Extractor Utility and Hive Table Cloner. Supported cost-effective, cross-region analytics.",
      type: "type2",
      icon: "🔧",
      link: "companies/6sense.html"
    },
    {
      company: "InCred",
      date: "Apr 2021 – Sep 2022",
      title: "Tech Lead - Data Engineer",
      // description:
      //   "Built the CDC and streaming platform using Spark, Kinesis, and DMS. Cut infra costs by 30%, improved refresh latency by 50%, and mentored junior engineers across BI and ML teams.",
      type: "type3",
      icon: "📊",
      link: "companies/incred.html"
    },
    {
      company: "Slice",
      date: "Nov 2019 – Apr 2021",
      title: "Lead Data Engineer",
      // description:
      //   "Built and scaled Slice Data Lake and the User Graph platform. Enabled graph-based risk scoring using AWS Neptune and Glue. Launched the in-house Slack alerting tool ‘Jarvis’.",
      type: "type1",
      icon: "📱",
      link: "companies/slice.html"
    },
    {
      company: "Particle41",
      date: "Nov 2016 – Oct 2019",
      title: "Software Developer → Data Engineer",
      // description:
      //   "Built Spark-based ETL pipelines, onboarding engine, and identity resolution graph. Led ad-ROI modeling and full-stack analytics dashboarding. Recognized for debugging and mentoring.",
      type: "type2",
      icon: "🧠",
      link: "companies/particle41.html"
    },
    {
      company: "Persistent Systems (Intern)",
      date: "Sep 2015 – Jul 2016",
      title: "Project Intern",
      // description:
      //   "Developed a stock market prediction tool using Django + technical indicators. Delivered end-to-end project aligned with Persistent’s academic mentorship program.",
      type: "type3",
      icon: "🎓",
      link: "companies/persistent.html"
    }
  ];

  experiences.forEach((exp, index) => {
    const eventEl = document.createElement("div");
    eventEl.className = `timeline__event animated fadeInUp delay-${3 - (index % 3)}s timeline__event--${exp.type}`;
    exp.description = "Click to know more"
    eventEl.innerHTML = `
      <div class="timeline__event__icon">
        <span style="font-size: 24px">${exp.icon}</span>
      </div>
      <div class="timeline__event__date">${exp.date}</div>
      <div class="timeline__event__content">
        <div class="timeline__event__title">${exp.title} @ ${exp.company}</div>
        <div class="timeline__event__description"><p>${exp.description}</p></div>
      </div>
    `;

    eventEl.style.cursor = "pointer";
    eventEl.addEventListener("click", () => {
      // Fetch company-specific HTML content and inject into modal
      if (exp.link) {
        fetch(exp.link)
          .then(res => res.text())
          .then(html => {
            modalBody.innerHTML = html;
            modal.classList.remove("hidden");
          })
          .catch(() => {
            modalBody.innerHTML = `<h2>${exp.company}</h2><p>Could not load details.</p>`;
            modal.classList.remove("hidden");
          });
      }
    });

    timelineContainer.appendChild(eventEl);
  });

  closeModalBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    modalBody.innerHTML = "";
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) {
      modal.classList.add("hidden");
      modalBody.innerHTML = "";
    }
  });
});