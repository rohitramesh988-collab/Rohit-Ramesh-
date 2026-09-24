/* =========================================================
   Digital Growth Solutions — AI Guide
   A lightweight, on-page assistant that helps visitors find
   the right service, pricing or portfolio information without
   having to navigate the whole site manually. It runs entirely
   in the browser against a curated knowledge base — it is not
   a live language model, and it says so, and it always hands
   real pricing negotiation, custom scopes and commercial
   decisions to Rohit directly rather than guessing.
   ========================================================= */

(function () {
  "use strict";

  var KB = [
    {
      id: "local-ai-search",
      keywords: ["local search", "google maps", "ai search", "chatgpt", "gemini", "claude", "ai visibility", "aeo", "geo", "answer engine", "show up on ai", "found on chatgpt"],
      title: "Local & AI Search Visibility",
      answer:
        "This service helps your business show up on Google Maps and on AI search tools such as ChatGPT, Gemini and Claude, when someone nearby asks about a business like yours. It's priced at ₹7,500 and covers setting up and optimising your business listings and structured information so both traditional and AI search engines can find and recommend you.",
      links: [{ href: "services.html#local-ai-search", label: "See what's included" }]
    },
    {
      id: "seo",
      keywords: ["seo", "google ranking", "rank higher", "search engine optimization", "organic traffic", "keywords"],
      title: "SEO",
      answer:
        "Basic SEO is priced at ₹4,500 a month and focuses on using the exact words your customers search for, so your website is found at the moment they're looking, rather than chasing rankings for terms nobody searches.",
      links: [{ href: "services.html#seo", label: "See what's included" }, { href: "about.html", label: "Read the approach behind it" }]
    },
    {
      id: "website",
      keywords: ["website", "wordpress", "web design", "web development", "new site", "landing page", "domain", "hosting"],
      title: "Website Development",
      answer:
        "A properly built WordPress website, working on any screen size and easy for Google to read, is priced at ₹6,000 for setup, domain and hosting configuration and plugin installation. Domain and hosting subscription costs are billed directly to you by the provider, so there's no markup.",
      links: [{ href: "services.html#website", label: "See what's included" }]
    },
    {
      id: "social",
      keywords: ["social media", "instagram", "facebook", "meta", "linkedin posts", "social posts"],
      title: "Social Media Marketing",
      answer:
        "Organic posts and graphics for one platform (Facebook, Instagram or LinkedIn) are priced at ₹4,000 per platform per month, covering regular photos and updates that keep your business visible to people already following you.",
      links: [{ href: "services.html#social", label: "See what's included" }]
    },
    {
      id: "video",
      keywords: ["video", "reels", "short video", "video content"],
      title: "Videos That Show Your Work",
      answer:
        "Short videos that show your work clearly, so customers feel confident choosing you, are priced at ₹3,000 per video.",
      links: [{ href: "services.html#video", label: "See what's included" }]
    },
    {
      id: "graphic-design",
      keywords: ["graphic design", "business card", "flyer", "brochure", "print", "logo"],
      title: "Graphic Design (on request)",
      answer:
        "Graphic design for business cards, flyers, brochures, labels and other print collateral is available on request at ₹3,000 and can be added alongside any core service.",
      links: [{ href: "services.html#extras", label: "See details" }]
    },
    {
      id: "content-marketing",
      keywords: ["content marketing", "blog", "newsletter", "copywriting", "content strategy"],
      title: "Content Marketing (on request)",
      answer:
        "Content marketing, covering new blogs, newsletters, content strategy and campaign copywriting, is available on request at ₹8,000 and can be added alongside any core service.",
      links: [{ href: "services.html#extras", label: "See details" }]
    },
    {
      id: "amc",
      keywords: ["amc", "annual maintenance", "ongoing support", "monthly retainer", "maintenance contract"],
      title: "Annual Maintenance Contract",
      answer:
        "If you'd prefer ongoing support instead of one-off projects, an Annual Maintenance Contract is available, priced monthly based on the number of services you'd like maintained. Pricing depends on your specific mix, so this is one for a direct conversation.",
      links: [{ href: "contact.html", label: "Ask about an AMC" }]
    },
    {
      id: "pricing-overview",
      keywords: ["price", "pricing", "cost", "how much", "rate", "rates", "budget", "fee", "charges"],
      title: "Pricing",
      answer:
        "Core services are priced individually so you only pay for what your business needs: Local & AI Search Visibility ₹7,500, SEO ₹4,500, Website Development ₹6,000, Social Media Marketing ₹4,000 per platform, and short-form Videos ₹3,000 per video. Graphic Design and Content Marketing are available on request. Everything is agreed in writing, timeline and result included, before any work starts.",
      links: [{ href: "services.html", label: "View the full price list" }]
    },
    {
      id: "process",
      keywords: ["process", "how it works", "how do you work", "steps", "get started", "onboarding", "timeline"],
      title: "How the work is structured",
      answer:
        "The process starts with how people actually search today, on Google, Google Maps and AI apps. Everything, timeline and result included, is agreed before any work begins. Only a few clients are taken on at a time so each business gets full attention, and you work directly with Rohit, no account managers or handoffs.",
      links: [{ href: "about.html#process", label: "Read the full process" }, { href: "contact.html", label: "Start a conversation" }]
    },
    {
      id: "portfolio",
      keywords: ["portfolio", "examples", "past work", "case study", "case studies", "sample work", "client work"],
      title: "Portfolio",
      answer:
        "Rohit Ramesh operates as an independent consultant, so the portfolio page focuses on the type of work delivered and the thinking behind it rather than a client showcase. If you'd like to see specific examples relevant to your industry, that's easiest to walk through on a direct call.",
      links: [{ href: "portfolio.html", label: "View the portfolio page" }]
    },
    {
      id: "testimonials",
      keywords: ["testimonial", "reviews", "review", "rating", "reference", "trust", "proof"],
      title: "Testimonials",
      answer:
        "You can find the current state of client feedback on the testimonials page, along with how references can be arranged directly. Nothing there is invented or exaggerated.",
      links: [{ href: "testimonials.html", label: "View testimonials" }]
    },
    {
      id: "about",
      keywords: ["who is rohit", "about rohit", "experience", "years", "background", "independent", "freelance", "agency or freelancer", "solo"],
      title: "About Rohit",
      answer:
        "Rohit Ramesh is an independent digital marketing consultant with 8 years of experience, working directly with each client rather than through an agency structure. No account managers, no handoffs, just one person who understands your business.",
      links: [{ href: "about.html", label: "Read Rohit's background" }]
    },
    {
      id: "industries",
      keywords: ["industry", "industries", "type of business", "small business", "startup", "b2b", "ecommerce", "real estate", "healthcare", "clinic", "restaurant"],
      title: "Who this is for",
      answer:
        "The services are built for small businesses, startups and growing companies, professional services, local businesses, B2B companies and founders who need practical, honest digital marketing rather than jargon. If you're unsure whether your business fits, describe it here and I'll point you the right way, or you can ask Rohit directly.",
      links: [{ href: "about.html", label: "Read who this is for" }, { href: "contact.html", label: "Describe your business" }]
    },
    {
      id: "contact",
      keywords: ["contact", "call", "whatsapp", "phone", "email", "reach", "talk to rohit", "speak to someone", "get in touch", "quote", "proposal", "hire", "custom pricing", "negotiate"],
      title: "Getting in touch",
      answer:
        "For quotes, custom scopes, negotiation or anything specific to your business, the fastest route is a direct conversation. Call or WhatsApp +91 81977 79500, email rohitramesh988@gmail.com, or use the contact form and Rohit will follow up personally.",
      links: [{ href: "contact.html", label: "Go to the contact page" }]
    },
    {
      id: "results",
      keywords: ["guarantee", "results", "roi", "promise", "how long", "when will i see"],
      title: "On guarantees and timelines",
      answer:
        "No SEO or search visibility work can honestly be guaranteed in a fixed timeframe, and it's worth being wary of anyone who promises exact rankings or results. What's offered instead is a clear, agreed scope and an honest plan based on how your customers actually search. Timelines are discussed openly once the situation is understood.",
      links: [{ href: "about.html", label: "Read the working philosophy" }]
    }
  ];

  var FALLBACK = {
    title: "Let's get you to the right place",
    answer:
      "I couldn't match that to something specific in what I know. You can browse Services & Pricing, Portfolio or About Me directly, or describe your business and what you're trying to fix, and Rohit will follow up personally.",
    links: [
      { href: "services.html", label: "Services & Pricing" },
      { href: "contact.html", label: "Contact Rohit" }
    ]
  };

  var SUGGESTIONS = [
    "What does SEO cost?",
    "Do you build websites?",
    "How does AI search visibility work?",
    "What's the process?",
    "How do I get in touch?"
  ];

  function score(text, entry) {
    var hits = 0;
    for (var i = 0; i < entry.keywords.length; i++) {
      if (text.indexOf(entry.keywords[i]) !== -1) {
        hits += entry.keywords[i].split(" ").length;
      }
    }
    return hits;
  }

  function findAnswer(query) {
    var text = query.toLowerCase();
    var best = null;
    var bestScore = 0;
    for (var i = 0; i < KB.length; i++) {
      var s = score(text, KB[i]);
      if (s > bestScore) {
        bestScore = s;
        best = KB[i];
      }
    }
    return best || FALLBACK;
  }

  function el(tag, className, html) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (html !== undefined) node.innerHTML = html;
    return node;
  }

  function buildLinksHtml(links) {
    if (!links || !links.length) return "";
    return (
      '<div style="margin-top:0.6rem;display:flex;flex-wrap:wrap;gap:0.5rem;">' +
      links
        .map(function (l) {
          return '<a href="' + l.href + '">' + l.label + " →</a>";
        })
        .join(" ") +
      "</div>"
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    var launcher = document.getElementById("ai-launcher");
    var panel = document.getElementById("ai-panel");
    var closeBtn = document.getElementById("ai-panel-close");
    var body = document.getElementById("ai-panel-body");
    var chips = document.getElementById("ai-chip-row");
    var form = document.getElementById("ai-panel-form");
    var input = document.getElementById("ai-panel-input");

    if (!launcher || !panel || !body || !form || !input) return;

    var opened = false;

    function addMessage(role, html) {
      var msg = el("div", "ai-msg ai-msg--" + role, html);
      body.appendChild(msg);
      body.scrollTop = body.scrollHeight;
    }

    function respond(query) {
      addMessage("user", query.replace(/</g, "&lt;"));
      var match = findAnswer(query);
      var html = "<strong>" + match.title + "</strong><br>" + match.answer + buildLinksHtml(match.links);
      window.setTimeout(function () {
        addMessage("bot", html);
      }, 220);
    }

    function openPanel() {
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      launcher.setAttribute("aria-expanded", "true");
      if (!opened) {
        opened = true;
        addMessage(
          "bot",
          "Hi, I'm the Digital Growth Solutions guide. I can help you find the right service, pricing or next step based on what your business needs. For quotes, custom scopes or anything that needs Rohit's judgement, I'll point you straight to him."
        );
        SUGGESTIONS.forEach(function (s) {
          var chip = el("button", "ai-chip", s);
          chip.type = "button";
          chip.addEventListener("click", function () {
            respond(s);
          });
          chips.appendChild(chip);
        });
      }
      input.focus();
    }

    function closePanel() {
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      launcher.setAttribute("aria-expanded", "false");
    }

    launcher.addEventListener("click", function () {
      if (panel.classList.contains("is-open")) {
        closePanel();
      } else {
        openPanel();
      }
    });

    closeBtn.addEventListener("click", closePanel);

    panel.addEventListener("click", function (e) {
      if (e.target === panel) closePanel();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && panel.classList.contains("is-open")) {
        closePanel();
      }
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var value = input.value.trim();
      if (!value) return;
      respond(value);
      input.value = "";
    });

    var autoOpenTrigger = document.querySelectorAll("[data-ai-open]");
    autoOpenTrigger.forEach(function (trigger) {
      trigger.addEventListener("click", function (e) {
        e.preventDefault();
        openPanel();
        var seed = trigger.getAttribute("data-ai-open");
        if (seed) {
          window.setTimeout(function () {
            respond(seed);
          }, 150);
        }
      });
    });
  });
})();
