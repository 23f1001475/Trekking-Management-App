<template>

    <div class = "container-fluid bg-light vh-100">
        <div>
            <div class = "row">
            <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm px-2">
                <div class="container-fluid">
                    <span class = "navbar-brand">

                        <strong>
                            Schedule Trek
                        </strong>
                    
                    </span>
                    <div class = "d-flex align-items-end">

                        <button @click = "emitManageTrek()" class = "btn btn-secondary me-3">
                            Manage Treks
                        </button>

                    
                    
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
                            Schedule Trek
                        </strong>
                    </div>
                    <div class = "card-body pb-1">

                        <form  @submit.prevent = "handleScheduleTrek">

                            <div class = "mb-3">

                                <label class = "form-label">
                                   Trek Name
                                </label>

                                <input :value ="trekName"  type = "text" placeholder = "Trek Name" class = "form-control" readonly>

                                <p v-for = "error in errors.trek_name" :key="error"  class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">

                                <label class = "form-label">
                                    Next Departure
                                </label>

                                <input v-model = "form.start_date" type = "date" placeholder = "Departure Date" class = "form-control">

                                <p v-for = "error in errors.start_date" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">

                                <label class = "form-label">
                                    End Date
                                </label>
                                
                                <input v-model = "form.end_date" type = "date" placeholder = "End Date" class = "form-control">
                                
                                <p v-for = "error in errors.end_date" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>

                            <div class = "mb-3">
                                <label class = "form-label">
                                    Total Slots
                                </label>
                                <input v-model = "form.total_slots" type = "number" placeholder = "Total Slots" class = "form-control">

                                <p v-for = "error in errors.total_slots" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>


                            <div class = "mb-3">
                                <label class = "form-label">
                                    Price
                                </label>
                                <input v-model = "form.price" type = "number" placeholder = "Price" class = "form-control">

                                <p v-for = "error in errors.price" :key = "error" class = "text-danger">
                                    {{ error }}
                                </p>

                            </div>
                            

                            <div class = "d-flex justify-content-center row mb-0 mt-5">
                            
                                <button  type = "submit" class = "btn btn-primary py-2 ">
                                    Schedule
                                </button>

                            </div>
                        </form>
                    </div> 
                </div>
            </div>
        </div>

        <div class = "d-flex justify-content-end me-4 mt-5">
            <button @click = "goBack()" class = "btn btn-lg btn-secondary">
                Go Back
            </button>
        </div>

    </div>

</template>

<script>

import axios from "axios";

export default {
    name: "ScheduleTrek",


    props: {
        "routeId": {
            type : Number,
            required : true
        },
        "trekName": {
            type : String,
            required : true
        },
    },

    data () {
        return {

            errors: {},
            form: {
                trek_name: this.trekName,
                start_date: "",
                end_date: "",
                total_slots: "",
                price: "",
                status : "open"
            }
            }
        },


    methods: {
        
        handleScheduleTrek() {


            this.errors = {};

            const token = localStorage.getItem("token");

            axios.post(`http://127.0.0.1:5000/api/admin/routes/${this.routeId}/schedule`, this.form,{
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
                .then((response) => {

                    alert("Trek Scheduled Successfully");
                    this.$emit("trek-scheduled", response.data);

            }).catch((error) => {

                if (error.response && error.response.status === 400){

                    this.errors = error.response.data.errors || {};

                }else if (error.response && error.response.status === 401){
                    alert("Your are not authorised to schedule a trek");
                }else{
                    alert("Something went wrong");
                }
            });
        },




        goBack() {
            this.$emit("go-back");
        },

        emitManageTrek() {
            this.$emit("manage-trek");
        },

        logout() {
            localStorage.removeItem("user");
            this.$router.replace({ name: 'Login' });

        }


    }
}


</script>
