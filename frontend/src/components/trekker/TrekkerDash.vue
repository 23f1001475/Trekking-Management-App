<template>
    <div class="container-fluid bg-light min-vh-100">

        <div class="row">

            <nav class="navbar navbar-expand-lg bg-white border-bottom px-2">

                <div class="container-fluid">

                    <span class="navbar-brand">

                        <h1 class="mt-2 fw-semibold display-5">

                            Welcome {{ user.username }}

                        </h1>
                        <p class="fw-semibold text-muted ms-1">

                            Browse available treks and track your booked treks

                        </p>
                    </span>
                    
                    <div class = "d-flex align-items-center gap-3">

                        <button @click = "emitProfile" class = "btn btn-border border-0 fw-semibold"  style = "font-size: 18px ; text-decoration: underline">
                            Profile
                        </button>

                        <button @click = "emitHistory" class = "btn btn-border border-0 fw-semibold"  style = "font-size: 18px ; text-decoration: underline">
                            History
                        </button>

                        <input v-model="searchText" type="search" class="form-control" placeholder="Search treks..." style="width: 280px">
                        
                        
                        <button @click="logout" class="btn btn-secondary btn-lg px-4">
                            Logout
                        </button>
                        
                    </div>
                </div>
            </nav>
        </div>


        <div class="container py-5">

            <div class="row g-4 mb-4 justify-content-center text-center">

                <div class="col-md-4">

                    <div class="card shadow-sm border-0 p-3">

                        <div class="card-body">

                            <p class="text-muted fw-semibold mb-2" style = "font-size: 20px">

                                Available Treks

                            </p>

                            <h2 class="fw-bold mb-0" style = "font-size: 40px">

                               {{ available_treks_count }}

                            </h2>
                            
                        </div>

                    </div>

                </div>
                <div class="col-md-4">

                    <div class="card shadow-sm border-0 p-3">

                        <div class="card-body">

                            <p class="text-muted fw-semibold mb-2" style = "font-size: 20px">

                                Booked Treks

                            </p>
                            <h2 class="fw-bold mb-0" style = "font-size: 40px">

                                {{ booked_treks_count }}

                            </h2>
                        </div>
                    </div>
                </div>

                
            </div>


            <div class="card shadow-sm border-0 mb-4">

                <div class="card-header bg-white border-bottom d-flex justify-content-between">

                    <div>

                        <h4 class="fw-semibold mb-0">

                        Available Treks

                        </h4>

                        <p class="text-muted fw-semibold mb-0">

                            Treks currently available for booking

                        </p>

                    </div>

                    
                    <div class = "d-flex gap-3">
                        <div>
                        <p class = "text-muted fw-semibold mb-0">
                            filter price
                        </p>
                   
                        <select v-model = "PriceFilter"  class="form-select mt-0" style = "width: 160px">

                            <option value="">All</option>
                            <option value="low_to_high">low to high</option>
                            <option value="high_to_low">high to low</option>
                            <option value="below_4000">below 4000</option>
                            <option value="below_8000">below 8000</option>

                        </select>
                        </div>
                        <div>
                    
                        <p class = "text-muted fw-semibold mb-0">

                            filter difficulty

                        </p>
                   
                        <select v-model = "DifficultyFilter"  class="form-select mt-0" style="width: 160px">
                            
                            <option value="">All</option>
                            <option value="Easy">Easy</option>
                            <option value="Moderate">Moderate</option>
                            <option value="Tough">Tough</option>

                        </select>
                        </div>
                    </div>
                    
                </div>

                <div class="card-body">

                    <div v-if = "filteredAvailableTreks.length === 0" class = "text-muted">

                        No available treks found.

                    </div>

                    <div v-else class = "table-responsive"  style = "max-height: 400px; overflow-y: auto;">
                        <table class = "table table-hover table-striped align-middle">
                            
                            <thead>

                                <tr>
                                    <th>Trek Name</th>
                                    <th>Start Date</th>
                                    <th>End Date</th>
                                    <th>Available Slots</th>
                                    <th>Price</th>
                                    <th>Difficulty</th>
                                    <th>Action</th>
                                </tr>

                            </thead>

                            <tbody>

                                <tr v-for = "trek in filteredAvailableTreks"  :key = "trek.trek_id">
                                    
                                    <td>
                                        {{ trek.trek_name }}
                                    </td>
                                    <td>
                                        {{ formatDate(trek.start_date) }}
                                    </td>
                                    <td>
                                        {{ formatDate(trek.end_date) }}
                                    </td>
                                    <td>
                                        {{ trek.available_slots }}
                                    </td>
                                    <td>
                                        {{ formatCurrency(trek.price) }}
                                    </td>
                                    <td>
                                        <span>

                                            {{ trek.difficulty }}

                                        </span>
                                    </td>
                                    <td>
                                        <button @click = "ViewTrek(trek.trek_id)" class="btn btn-primary">
                                            Book Now
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm border-0 mb-5">

                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        Booked Treks
                    </h4>

                    <p class="text-muted fw-semibold mb-0">
                        Treks you have already booked
                    </p>

                </div>

                <div class="card-body">

                    <div v-if="filteredBookedTreks.length === 0" class="text-muted">

                        No booked treks found.

                    </div>

                    <div v-else class="table-responsive"  style = "max-height: 400px; overflow-y: auto;">

                        <table class="table table-hover table-striped align-middle">

                            <thead>

                                <tr>
                                    <th>Trek Name</th>
                                    <th>Booking Date</th>
                                    <th>start Date</th>
                                    <th>End Date</th>
                                    <th>Booking Status</th>
                                    <th>Difficulty</th>
                                    <th>Action</th>
                                </tr>

                            </thead>

                            <tbody>

                                <tr v-for="booking in filteredBookedTreks" :key = "booking.booking_id">
                                    
                                    <td>
                                        {{ booking.trek_name }}
                                    </td>

                                    <td>
                                        {{ formatDate(booking.booking_date) }}
                                    </td>

                                    <td>
                                        {{ formatDate(booking.start_date) }}
                                    </td>

                                    <td>
                                        {{ formatDate(booking.end_date) }}
                                    </td>

                                    <td>
                                        {{ booking.status }}
                                    </td>

                                    <td>

                                            {{ booking.difficulty }}
                                        
                                    </td>

                                    <td>
                                        <button @click = "CancelBooking(booking.booking_id)" class="btn btn-danger">
                                            Cancle
                                        </button>
                                    </td>

                                </tr>

                            </tbody>

                        </table>

                    </div>

                </div>

            </div>
        </div>
    </div>
</template>



<script>

import axios from "axios";


import TrekHistory from "@/components/trekker/TrekHistory.vue";

import TrekkerProfile from "@/components/trekker/TrekkerProfile.vue";

import BookTrek from "@/components/trekker/BookTrek.vue";

export default {

    name: "TrekkerDash",


    data() {
        return {
            user: JSON.parse(localStorage.getItem('user')),

        trekkerName: "",
        searchText: "",
        PriceFilter: "",
        DifficultyFilter: "",
        available_treks_count: 0,
        booked_treks_count: 0,
        availableTreks: [],
        bookedTreks: []

        };
    },


    components: {

        TrekHistory,
        TrekkerProfile,
        BookTrek
    },



    computed: {

            filteredAvailableTreks() {

                let treks = [...this.availableTreks];

                const search = this.searchText.trim().toLowerCase();

                if (search) {

                    treks = treks.filter((trek) => {

                        return [

                            trek.trek_name,
                            // trek.start_date,
                            // trek.end_date,
                            // trek.status,
                            // trek.price,
                            // trek.difficulty
                        ].join(" ").toLowerCase().includes(search);

                    });
                }

                if (this.DifficultyFilter) {

                    treks = treks.filter((trek) => {

                        return trek.difficulty === this.DifficultyFilter;

                    });
                }

                if (this.PriceFilter === "below_4000") {

                    treks = treks.filter((trek) => Number(trek.price) < 4000);

                }
                if (this.PriceFilter === "below_8000") {

                    treks = treks.filter((trek) => Number(trek.price) < 8000);

                }
                if (this.PriceFilter === "low_to_high") {

                    treks = treks.sort((a, b) => Number(a.price) - Number(b.price));

                }
                if (this.PriceFilter === "high_to_low") {

                    treks = treks.sort((a, b) => Number(b.price) - Number(a.price));

                }

                return treks;
            },
        filteredBookedTreks() {

            const search = this.searchText.trim().toLowerCase();

            if (!search) {
                return this.bookedTreks;
            }
            return this.bookedTreks.filter((booking) => {

                return [

                    
                    booking.trek_name,
                    // booking.start_date,
                    // booking.end_date,
                    // booking.status

                ].join(" ").toLowerCase().includes(search);

            });
        },
        
    },


    mounted() {
        this.fetchDashboard();
    },



    methods: {
        async fetchDashboard() {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.get("http://127.0.0.1:5000/api/trekkers/dashboard", {

                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                });
                if (res.status === 200) {

                    console.log(res.data);
                    this.availableTreks = res.data.available_treks;
                    this.bookedTreks = res.data.booked_treks;
                    this.available_treks_count = res.data.available_treks_count;
                    this.booked_treks_count = res.data.booked_treks_count;

                }
            } catch (error) {

                console.error("Error fetching user dashboard:", error);

            }

        },

        formatDate(dateValue) {

            if (!dateValue) return "-";

            return String(dateValue).slice(0, 10);

        },

        formatCurrency(amount) {
            return `₹${Number(amount || 0).toFixed(2)}`;
        },




        ViewTrek(trek_id) {
            this.$emit("book-now-trek", trek_id);
        },


        async CancelBooking(booking_id) {

            try {

                const token = localStorage.getItem("token");

                await axios.post(`http://127.0.0.1:5000/api/trekkers/bookings/${booking_id}/cancel`,{}, {

                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                });

                alert("Booking Cancelled Successfully");
                this.fetchDashboard();               // this will refresh the dashboard data

            } catch (error) {   

                console.error("Error cancelling booking:", error);
                alert("Booking cancellation failed. Please try again.");

            }

        },

            

        

        logout() {

            localStorage.removeItem("user");
            this.$router.replace({ name: "Login" });
        },


        emitProfile () {
            this.$emit('show-profile');
        },

        emitHistory () {
            this.$emit('show-history');
        }
    }
};
</script>

