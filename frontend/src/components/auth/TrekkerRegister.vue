
<template>
<div style = "background-image : url('src/styles/images/log_reg.png'); background-size: cover; background-position: center center">
    <div class = "container vh-100 d-flex justify-content-center align-items-center">

        <div class = "card shadow p-4 rounded-4" style = "width: 450px; background-color: #E8EFF0">

            <h3 class="text-center mb-3">
                SummitGo
            </h3>

            <p class="text-center text-muted">
                Join us and start your adventure
            </p>

            <form @submit.prevent = "handleRegister">

                <div class = "mb-3">

                    <input
                        type = "text"
                        class = "form-control"
                        placeholder = "Full Name"
                        v-model = "form.username"
                    />
                    <p v-for = "error in errors.username" :key = "error" class = "text-danger">
                        {{ error }}
                    </p>

                </div>

                <div class = "mb-3">

                    <input
                        type = "email"
                        class = "form-control"
                        placeholder = "Email"
                        v-model = "form.email"
                    />

                    <p v-for = "error in errors.email" :key = "error" class = "text-danger">
                        {{ error }}
                    </p>

                </div>

                <div class = "mb-3">

                    <input
                        type = "text"
                        class = "form-control"
                        placeholder = "Phone Number"
                        v-model = "form.phone"
                    />

                    <p v-for = "error in errors.phone" :key = "error" class = "text-danger">
                        {{ error }}
                    </p>  

                </div>

                <div class = "mb-3">
                    <input
                      type = "password"
                      class = "form-control"
                      placeholder = "Password"
                      v-model = "form.password"
                    />

                    <p v-for = "error in errors.password" :key = "error" class = "text-danger">
                        {{ error }}
                    </p>
                    
                </div>

                <div class = "mb-3">
                    <input
                      type = "password"
                      class = "form-control"
                      placeholder = "Confirm Password"
                      v-model = "form.password_confirm"
                    />
                </div>

                <button class = "btn btn-dark w-100" type = "submit">

                  Register

                </button>

                <div class = "text-center mt-3">

                    Already have an account?

                    <a href="#" @click.prevent="$router.push('/login')">

                        Login

                    </a>

                </div>

            </form>
        </div>
    </div>
</div>
</template>

<script>
import axios from "axios";

export default {
  name: "UserRegister",
  emits: ["registered", "login-link-clicked"],

  data() {
    return {
      form: {
        username: "",
        email: "",
        phone: "",
        role: "trekker",
        password: "",
        password_confirm: ""
      },

      errors: {}
    };
  },

  methods: {
    handleRegister() {
      this.errors = {};

      if (this.form.password !== this.form.password_confirm) {
        alert("Passwords do not match");
        return;
      }

      axios.post("http://127.0.0.1:5000/api/register", this.form)
        .then((response) => {

          this.$emit("registered", response.data);

        })
        .catch((error) => {
          if (error.response && error.response.status === 400){
            this.errors = error.response.data;
          }
          else {
            alert("Registration Failed");
          }
          

        });
    }
  }
};
</script>