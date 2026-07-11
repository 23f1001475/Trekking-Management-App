<template>
    <div class = "container-fluid bg-light vh-min-100">
        <div class = "bg-light vh-100">
            <div class = "row">
                <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">

                    <div class = "container-fluid">

                        <span class = "navbar-brand">
                            <div class = "fw-semibold display-4">
                                Trekker Profile
                            </div>
                        </span>

                        <div class = "d-flex align-items-center">
                            <button @click = "goBack()" class = "btn btn-secondary">
                                Go Back
                            </button>
                        </div>
                    </div>
                </nav>        

            </div>

            <div class = "container mt-5">

                <div class = "card shadow-sm border ">
                    <div class = "card-header text-center">
                        <strong class = "fw-bold display-6">
                            Trekker Profile
                        </strong>
                    </div>
                    <div class = "card-body">
                        
                        <div class="row border-bottom mb-2 pb-2">
                            <div class = "col">
                                <div class = "fw-bold">
                                    
                                </div>
                            </div>
                            <div class = "col">
                                <div class = "fw-bold">
                                    Trekker Details
                                </div>
                            </div>
                            <div class = "col">
                                <div class = "fw-bold">
                                    Update Details
                                </div>
                                
                            </div>
                        </div>

                        <div class = "row border-bottom mb-2">
                            <div class = "col align-self-center"  >
                                <div class = "fw-bold">
                                    Name:
                                </div>
                            </div>
                            <div class = "col align-self-center">
                                <div class = "fw-semibold">
                                    {{ trekker_name }}
                                </div>
                            </div>
                            <div class = "col align-self-center pb-2">

                                <input v-model = "trekker_name" type = "text" placeholder = "change name" class = "form-control">        
                                
                            </div>
                        </div>

                        <div class = "row border-bottom mb-2">
                            <div class = "col align-self-center"  >
                                <div class = "fw-bold">
                                    Email :
                                </div>
                            </div>
                            <div class = "col align-self-center">
                                <div class = "fw-semibold">
                                    {{ trekker_email }}
                                </div>
                            </div>
                            <div class = "col align-self-center pb-2">

                                <input v-model="trekker_email" type = "email" placeholder = "change email" class = "form-control">        
                                
                            </div>
                        </div>

                        <div class = "row border-bottom mb-2">
                            <div class = "col align-self-center"  >
                                <div class = "fw-bold">
                                    Phone :
                                </div>
                            </div>
                            <div class = "col align-self-center">
                                <div class = "fw-semibold">
                                    {{ trekker_phone }}
                                </div>
                            </div>
                            <div  class = "col align-self-center pb-2">

                                <input v-model = "trekker_phone" type = "text" placeholder = "change phone" class = "form-control">        
                                
                            </div>
                        </div>

                        

                        

                    </div>

                    <div class = "card-footer text-center">

                        <button @click = "updateProfile" class = "btn btn-primary w-100">
                            Save Changes
                        </button>
                    </div>
                </div>
            
            </div>
        </div>
    

            
    </div>
</template>


<script>
import axios from "axios"; 

export default {
    name: "TrekkerProfile",



    data () {
        return {
            trekker_name : "",
            trekker_email : "",
            trekker_phone : "",            
        }
    },

    mounted() {
        this.getProfile()
    },


    methods : {
        goBack() {
            this.$emit("go-back");
        },

        async getProfile(){

            try {
                const token = localStorage.getItem("token");

                // const userID = localStorage.getItem("user_id");

                const res = await axios.get(`http://127.0.0.1:5000/api/trekkers/profile`, 
                {
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });

                if (res.status === 200) {
                    this.trekker_name = res.data.username,
                    this.trekker_email = res.data.email,
                    this.trekker_phone = res.data.phone

                    }

            } catch (error) {
                console.error("Error fetching trekker profile:", error);    
            }
        },

        async updateProfile() {

            try {
                const token = localStorage.getItem("token");
                // const userID = localStorage.getItem("user_id");

                const res = await axios.put(`http://127.0.0.1:5000/api/trekkers/profile`, 
                {
                    username : this.trekker_name,
                    email : this.trekker_email,
                    phone : this.trekker_phone
                },
                {
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });

                if (res.status === 200) {

                    alert("Trekker profile updated successfully");
                }

                
            }
            

            catch (error) {
                if (error.response) {
                    alert(error.response.data.msg);
                }else{

                    alert("Something went wrong");
                }
                
            }
    
        }
    }


}
</script>