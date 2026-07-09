<template>
    <div class = "container-fluid bg-light vh-100">
        <div class = "row bg-light">
            <nav class = "navbar navbar-expand-lg bg-white px-2 border-bottom">
                <div class = "container-fluid">
                    <div class = "navbar-brand fw-bold">
                     Create Staff 
                    </div>

                    <div class = "d-flex align-items-end">

                        <button @click = "emitTrekStaff" class = "btn btn-transparent fw-semibold me-2">
                            Trek Staff
                        </button>
                        <button @click = "logout()" class = "btn btn-secondary">
                            Logout
                        </button>
                    </div>
                </div>
            </nav>
        

            <div class = "mt-5 bg-light" style = "width : 600px; margin-left: auto; margin-right: auto">
                <div class = "card shadow-sm border">
                    <div class = "card-header text-center">
                        <strong class = "fw-bold display-6">
                            Create Staff
                        </strong>
                    </div>
                    <div class = "card-body pb-1">
                        <form @submit.prevent = "handleCreateStaff">
                            <div class = "mb-3">

                                <label class = "form-label">
                                    Name
                                </label>

                                <input v-model = "form.staff_name" type = "text" placeholder = "Full Name" class = "form-control">

                                <p v-for = "error in errors.staff_name" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>
                            <div class = "mb-3">

                                <label class = "form-label">
                                    Email
                                </label>

                                <input v-model  = "form.staff_email" type = "email" placeholder = "Email" class = "form-control">

                                <p v-for = "error in errors.staff_email" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>
                            <div class = "mb-3">

                                <label class = "form-label">
                                    Phone
                                </label>

                                <input v-model = "form.staff_phone" type = "text" placeholder = "Phone" class = "form-control">
                                
                                <p v-for = "error in errors.staff_phone" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">
                                <label class = "form-label">
                                    Password
                                </label>
                                <input v-model = "form.staff_password" type = "password" placeholder = "Password" class = "form-control">

                                <p v-for = "error in errors.staff_password" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>
                            <div class = "mb-3">
                                <label class = "form-label">
                                    Confirm Password
                                </label>
                                <input v-model = "form.staff_password_confirm" type = "password" placeholder = "Confirm Password" class = "form-control">
                            </div>

                            <div class = "d-flex justify-content-center row mb-0">
                            
                                <button  type = "submit" class = "btn btn-primary ">
                                    Create
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

    
            </div>
            <div class = "mt-5 me-1 d-flex justify-content-end ">
                    <button @click="goBack" class = "btn btn-secondary">
                        Go Back
                    </button>
            </div>
        </div>
        
    </div>
</template>




<script>

import axios from "axios";

export default {
    name: "CreateStaff",


    data () {
        return {
            errors : {},
            form  : {
                staff_name : "",
                staff_email : "",
                staff_phone : "",
                role : "trek_staff",
                staff_password : "",
                staff_password_confirm : ""
            }
        }
    },

    methods : {


        handleCreateStaff () {
            this.errors = {};

            if (this.form.staff_password !== this.form.staff_password_confirm) {
                alert("Passwords do not match");
                return;
            }

            const token = localStorage.getItem("token");

            axios.post("http://127.0.0.1:5000/api/admin/create_staff", this.form, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
                .then((response) => {

                    alert("Staff Created Successfully");
                    this.$emit("staff-created", response.data);

                })
                .catch((error) => {

                    if (error.response) {
                        if (error.response.status === 400) {

                            this.errors = error.response.data;

                        } else if (error.response.status === 401) {

                            alert("Unauthorized — please login as admin");
                            this.$router.push('/login');

                        } else {

                            alert("Staff Creation Failed");

                        }
                    } else {

                        alert("Staff Creation Failed");
                    }
                });
        },


       



        emitTrekStaff () {
            this.$emit('show-staff');
        },

        goBack () {
            this.$emit('go-back');
        },

        logout() {
            localStorage.removeItem("user");
            this.$router.replace({ name: 'Login' });

        },

        staffCreate () {
            this.$emit('staff-created');
        }
    }

}
</script>
