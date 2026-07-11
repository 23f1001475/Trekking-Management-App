<template>
    <div class = "container-fluid bg-light min-vh-100">
        <div class = "row">
            <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">
                <div class = "container-fluid">
                    <span class = "navbar-brand">
                        <div class = "fw-semibold display-3">
                            {{ trek.trek_name }}
                        </div>

                        <p class = "fw-semibold text-muted ms-1">
                            Book your trek
                        </p>
                    </span>
                    <div class = "d-flex align-items-center">
                        <button @click = "logout()" class = "btn btn-secondary">
                            Logout
                        </button>
                        <button @click = "goBack()" class = "btn btn-secondary ms-2">
                            Go Back
                        </button>
                    </div>
                </div>
            </nav>

        </div>
        <div class = "container">
            
            <div class = "card shadow-sm border border-0 pb-3 mt-5">

                <div class = "card-header bg-white border-bottom text-center">

                    <h4 class = "fw-semibold">
                        Book Trek
                    </h4>

                    <div  style = "height : 400px">
                        <img :src = "trek.image"   class = "img-fluid rounded" style = "width: 100%; height: 100%; object-fit: cover;">              

                    </div>

                </div>
                <div class = "card-body">
                    
                    <div class = "card shadow-sm border border-0 p-2 mb-2">
                        <div class ="row">
                            <p class = "fw-semibold col-3 pt-1">
                                Description : 
                            </p>
                            <p class = "col-9 pt-1"> {{ trek.description || 'No description available' }}</p>
                        </div>
                    </div>

                    <div class = "card shadow-sm border border-0 p-2 ">
    
                        <div class = "border-bottom">
                            <div class ="row">
                                <p class = "fw-semibold col-3 pt-1">
                                    Location : 
                                </p>
                                <p class = "col-9 pt-1">{{ trek.location || 'Location not specified' }}</p>
                            </div>
                        </div>

                        <div class = "border-bottom ">
                            <div class ="row ">
                                <p class = "fw-semibold col-3 pt-1">
                                    Start Date : 
                                </p>
                                <p class = "col-9 pt-1">{{ formatDate(trek.start_date) }}</p>
                            </div>
                        </div>
                        
                        <div class = "border-bottom ">
                            <div class = "row" >  
                                <p class = "fw-semibold col-3 pt-1">
                                    End Date : 
                                </p>
                                <p class = "col-9 pt-1">{{ formatDate(trek.end_date) }}</p>
                            </div>
                        </div>

                        <div class= "border-bottom">
                            <div class = "row">
                                <p class = "fw-semibold col-3 pt-1">
                                    Difficulty : 
                                </p>
                                <p class = "col-9 pt-1">{{ trek.difficulty}}</p>
                            </div>
                        </div>

                        <div class= "border-bottom">
                            <div class = "row">
                                <p class = "fw-semibold col-3 pt-1">
                                    Available Slots : 
                                </p>
                                <p class= "col-9 pt-1">{{ trek.available_slots || 0 }}</p>
                            </div>
                        </div>

                        <div class= "border-bottom">
                            <div class = "row">
                                <p class = "fw-semibold col-3 pt-1">
                                    Altitude : 
                                </p>
                                <p class = "col-9 pt-1">{{ trek.altitude }} ft</p>
                            </div>
                        </div>

                        <div class= "border-bottom">
                            <div class = "row">
                                <p class = "fw-semibold col-3 pt-1">
                                    Price : 
                                </p>
                                <p class = "col-9 pt-1">{{ formatCurrency(trek.price)}}</p>
                            </div>
                        </div>
                    </div>

                </div>
                <div class = "row mx-3">
                        <button @click = "confirmBooking()" class = "btn shadow-sm" style = "background-color :coral; color : white ; border-color:chocolate">
                            Book Now
                        </button>
                </div>


                    
            </div>
        </div>
        <div style = "height : 200px">
                
            </div>
    </div>
</template>




<script>
import axios from "axios";

export default {
    name : "BookTrek",


    props : {
        trekId : {

            type :[Number],
            required : true
        },

    },

    
    data () {
        return {

            trek :{},


        }
    },

    mounted () {
        this.fetchTrekDetails();
    },
    



    methods : {

        async fetchTrekDetails () {

            try {
                const token = localStorage.getItem("token");

                console.log("trekID", this.trekID);

                const res = await axios.get(

                    `http://127.0.0.1:5000/api/trekkers/treks/${this.trekId}`, {

                        headers: {
                            Authorization : `Bearer ${token}`
                        }  
                
                    }
                );

                this.trek = res.data.trek;
                


                } catch (error) {

                    console.error("Error fetching trek details:", error);
                    alert("Failed to load trek details.");
                    
                }
        },

        async confirmBooking () {

        try {

            const token = localStorage.getItem("token");

            await axios.post( "http://127.0.0.1:5000/api/trekkers/bookings" , {

                trek_id : this.trekId
            },
            {
                headers : {
                    Authorization : `Bearer ${token}`
                }
            }
        );
          alert("Trek Booked Successfully");

          this.trek.available_slots-- ;

          if (this.trek.available_slots === 0) {

            alert("Trek is fully booked. Please choose another trek.");

          }

        

        } catch (error) {

            console.error("Error booking trek:", error);
            alert("Booking failed. Please try again.");


        }

    },


    goBack() {
        this.$emit("back-to-dashboard");
    },

    formatDate(date) {
        return date ?date.slice(0, 10) : "";    //to conver the date from "YYYY-MM-DD : HH-MM" to "YYYY-MM-DD"  need to compulsarily pass the condition here is bwcause when the page is loaded(vue renders this component) api has not finished yet so the {{formatdate(start_date)}} is undefined and will throw error
    },

    formatCurrency(amount) {
        return `₹${Number(amount)}`;

    },

    logout () {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        this.$router.replace({ name: "Login" });
    }
            
    }

    

   
}
</script>


