document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          let validation = false;
          if (this.currentStep === 1){
            validation = this.validate_category()
          }
          else if(this.currentStep === 2)
          {
            validation = this.validate_bags()
          }
          else if(this.currentStep === 3)
          {
            validation = this.validate_institutions()
          }
          else if(this.currentStep === 4)
          {
            validation = this.validate_pick_up_data()
          }

          if(validation)
          {
            this.currentStep++;
            this.updateForm();
          } else {
            alert('Uzupełnij dane')
          }

        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      if (this.currentStep === 2) {
        const category_checkboxes = document.querySelectorAll("input[name='categories']:checked");
        let chckbox_values = [];
        category_checkboxes.forEach((checkbox) => {
          chckbox_values.push(checkbox.value);
        });

        var values = {categories: chckbox_values};
        var address = '/get_institutions/'
        $.ajax({
          url: address,
          data: values,
          method: 'GET',
          traditional: true,
          success: function (response) {
            var inst_div = document.getElementById("institutions_")
            inst_div.innerHTML = response
          },
          error: function (xhr, errmsg, err) {
            console.log("error")
            console.log(err, errmsg)
          }
        });
      }

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

      // TODO: get data from inputs and show them in summary

      var bags_num = $("#input-bags").val();
      var categories = $(".category-chckbox:checked").nextAll(".description").text()
      var institution_name = $(".institution-radio:checked").nextAll(".description").children(".title").text()
      var street_name = $("#input-street").val();
      var city_name = $("#input-city").val();
      var postcode = $("#input-postcode").val();
      var phone_num = $("#input-phone").val();
      var pickup_date = $("#input-date").val();
      var pickup_time = $("#input-time").val();
      var message = $("#input-text").val();

      $("#summary-bags").text(bags_num)
      $("#summary-checkboxes").text(categories)
      $("#summary-institution").text(institution_name);
      $("#summary-street").text(street_name);
      $("#summary-city").text(city_name);
      $("#summary-postcode").text(postcode);
      $("#summary-phone").text(phone_num);
      $("#summary-date").text(pickup_date);
      $("#summary-time").text(pickup_time);
      $("#summary-text").text("Uwagi: " + message);
    }

    validate_category() {
       const category_checkboxes = document.querySelectorAll("input[name='categories']:checked");
       return category_checkboxes.length > 0;
      };

    validate_bags() {
      const bags = document.getElementById("input-bags");
      return bags.value > 0 && bags.value !== ''
    };

    validate_institutions() {
      return document.querySelector(".institution-radio:checked");
    };

    validate_pick_up_data() {
      var street_name = document.querySelector("#input-street");
      var city_name = document.querySelector("#input-city");
      var postcode = document.querySelector("#input-postcode");
      var phone_num = document.querySelector("#input-phone");
      var pick_up_date = document.querySelector("#input-date");
      var pick_up_time = document.querySelector("#input-time");
      return street_name.value !== '' && city_name.value !== '' && postcode.value !== '' && phone_num.value !== '' &&
          pick_up_date.value !== '' && pick_up_time.value !== ''
    };


    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */


    submit(e) {
      // e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  var status = document.querySelectorAll(".donation-status_");

    status.forEach(s => {
      if (s.innerText === 'Tak') {
        var row = s.closest(".donation-row_")
        row.style.color = 'gray'
      }
    })
});
