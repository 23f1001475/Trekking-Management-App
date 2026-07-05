<template>
<div  style = "background-image : url('src/styles/images/log_reg.png'); background-size: cover; background-position: center center">
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div>
    <div class="text-center mb-3">

      <h2 class="fw-bold display-7 " >
        SummitGo
      </h2>

    </div>
    <div class = "card shadow rounded-4 p-4" style = "width : 400px; background-color: #E8EFF0;">

      <h3 class = "text-center mb-3">

        Welcome Back

      </h3>

      <form @submit.prevent = "handleLogin">

        <div class = "mb-3">
          <input

            class="form-control"
            placeholder="Email / Username"
            v-model="form.username"

          />
        </div>

        <div class="mb-3">
          <input

            type="password"
            class="form-control"
            placeholder="Password"
            v-model="form.password"

          />
        </div>

        <button class = "btn btn-dark w-100" type = "submit">
          Login
        </button>

        <div class="text-center mt-3">

          Don't have an account?

          <a href="#" @click.prevent="$router.push('/register')">

            Register

          </a>

        </div>

      </form>

    </div>
    </div>
  </div>
</div>
</template>

<script>

import axios from "axios";

export default {
  name: "Login",

  data() {

    return {

      form: {
        username: "",
        password: ""
      }
      
    };
  },

  methods: {
    handleLogin() {

      axios.post( "http://127.0.0.1:5000/api/login", this.form)
        .then((response) => {

          console.log("Login Success", response.data);

          localStorage.setItem("token", response.data.access_token);

          localStorage.setItem("user", JSON.stringify(response.data.user));

          if (response.data.role === "admin") {

            this.$router.push("/admin");

          }

          else if (

            response.data.role === "trek_staff"

          ) {

            this.$router.push("/staff");

          }

          else {

            this.$router.push("/user");

          }

        })
        .catch((error) => {

          console.error(error);

          alert("Login Failed");

        });

    }
  }
};
</script>
