<template>
    <div class = "container-fluid bg-light vh-100">
        <div>
            <div class = "row">
            <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm px-2">
                <div class="container-fluid">
                    <span class = "navbar-brand">

                        <strong>
                            Create Trek
                        </strong>
                    
                    </span>
                    <div class = "d-flex align-items-end">
                        <button @click = "emitManageTrek()" class = "btn btn-secondary">
                            Manage Treks
                        </button>

                    </div>
                    <div class = "d-flex align-items-end">
                        <button @click = "logout()" class = "btn btn-secondary">
                            Logout
                        </button>

                    </div>
                </div>
            </nav>
            </div>
            <div class = "continer-fluid" style = "margin-top: 50px; width : 600px; margin-left: auto; margin-right: auto">
                <div class = "card shadow-sm border">
                    <div class = "card-header text-center">
                        <strong class = "fw-bold display-6">
                            Create Trek
                        </strong>
                    </div>
                    <div class = "card-body pb-1">

                        <form @submit.prevent = "handleCreateTrek">

                            <div class = "mb-3">

                                <label class = "form-label">
                                   Trek Name
                                </label>

                                <input v-model = "form.route_name" type = "text" placeholder = "Trek Name" class = "form-control">

                                <p v-for = "error in errors.route_name" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">

                                <label class = "form-label">
                                    Location
                                </label>

                                <input v-model  = "form.location" type = "text" placeholder = "Location" class = "form-control">

                                <p v-for = "error in errors.location" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">

                                <label class = "form-label">
                                    Difficulty
                                </label>
                                <select v-model = "form.difficulty" placeholder = "Select Difficulty" class = "form-control">
                                    <option value = "Easy">Easy</option>
                                    <option value = "Moderate">Moderate</option>
                                    <option value = "Tough">Tough</option>
                                </select>
                                <!-- <input v-model = "form.difficulty" type = "text" placeholder = "Difficulty" class = "form-control"> -->
                                
                                <p v-for = "error in errors.difficulty" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">
                                <label class = "form-label">
                                    Duration
                                </label>
                                <input v-model = "form.days_on_trail" type = "number" placeholder = "Days of trail" class = "form-control">

                                <p v-for = "error in errors.days_on_trail" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>


                            <div class = "mb-3">
                                <label class = "form-label">
                                    Altitude
                                </label>
                                <input v-model = "form.altitude" type = "number" placeholder = "Altitude" class = "form-control">

                                <p v-for = "error in errors.altitude" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">
                                <label class = "form-label">
                                    Description
                                </label>
                                <input v-model = "form.description" type = "text" placeholder = "Description" class = "form-control">
                                
                                <p v-for = "error in errors.description" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>


                            <div class = "mb-3">
                                <label class = "form-label">
                                    Image
                                </label>
                                <input @change = "handleFileUpload" type = "file" placeholder = "Image" class = "form-control">
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
            <div>
                <button @click = "goBack()" class = "btn btn-secondary">
                    Go Back
                </button>
            </div>
        </div>
    </div>



</template>

<script>

import axios from "axios";

export default {
    name: "CreateTrek",


    data () {
        return {
            errors: {},
            form: {
                route_name: "",
                location: "",
                difficulty: "",
                days_on_trail: "",
                altitude: "",
                description: "",
                image: null
            }
        };
    },


    methods: {

        handleCreateTrek() {

            this.errors = {};


            const token = localStorage.getItem("token");

            const formData = new FormData();

            formData.append("route_name", this.form.route_name);
            formData.append("location", this.form.location);
            formData.append("difficulty", this.form.difficulty);
            formData.append("days_on_trail", this.form.days_on_trail);
            formData.append("altitude", this.form.altitude);
            formData.append("description", this.form.description);
                
            if (this.form.image) {
                formData.append("image", this.form.image);
            }



            axios.post("http://127.0.0.1:5000/api/admin/create_trek_route", formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "multipart/form-data"
                }
            })
                .then((response) => {
                    alert("Trek Created Successfully");
                    this.$emit("trek-created", response.data);

                })
                .catch((error) => {
                    if(error.response.status === 400){

                    this.errors = error.response.data.errors;
                }
                else if (error.response.status === 401){
                    alert("You are not authorized to create a trek route");
                    this.$router.push("/login");
                } else {

                    alert("Trek Creation Failed");
                }
            });
        },


        handleFileUpload(event) {

                        this.form.image = event.target.files[0];
        },


        trekCreated(trek) {
            this.$emit("trek-created", trek);
        },

        logout () {
            localStorage.removeItem("token");
            this.$router.push("/login");
        },


        goBack() {
            this.$emit("go-back");
        },

        emitManageTrek() {
            this.$emit("manage-trek");
        }
    }
}


</script>