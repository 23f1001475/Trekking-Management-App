
<template>
<div class="container-fluid bg-light vh-100">
    <div class = "row">
        <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">
            <div class="container-fluid">

                <span class="navbar-brand">
                    Welcome {{ user.username }}
                </span>

                <div class="d-flex align-items-center">

                    <button @click = "emitReports" class = "btn btn-transparent fw-semibold me-2">
                         Reports
                     </button>
                    <button @click = "emitTrekker" class = "btn btn-transparent fw-semibold me-2"> 
                        Trekkers
                    </button>
                    <button @click = "emitTrekStaff" class = "btn btn-transparent fw-semibold me-3">
                         Trek Staff 
                    </button>

                    <form class="d-flex me-3">

                        <input  v-model = "searchText" class = "form-control me-2" type = "search" placeholder = "Search"  >
                       
                    </form>
                    
                    <button @click = "logout()" class="btn btn-secondary">
                        Logout
                    </button>

                </div>

            </div>
        </nav>
    </div>
    <div class = "row  p-3"> 
        

        <div class="container bg-light py-4">

            <div class="row g-3 mb-4">

                <div class="col-md-3 col-lg">

                    <div class="card text-center">

                        <div class="card-body">

                            <h6 class = "fw-bold">
                                Total Treks
                            </h6>
                            <h3 >
                              {{total_treks}}
                            </h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-3 col-lg">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class = "fw-bold">
                                Active Treks
                            </h6>
                            <h3 >
                                {{ active_treks }}
                            </h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-3 col-lg">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class = "fw-bold">
                                Total Bookings
                            </h6>
                            <h3>
                                {{ total_bookings }}
                            </h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-3 col-lg">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class = "fw-bold">
                                Total Staff
                            </h6>
                            <h3>
                                {{ total_staff }}
                            </h3>
                        </div>
                    </div>
                </div>

                <div class="col-md-3 col-lg">
                    <div class="card text-center">
                        <div class="card-body">
                            <h6 class = "fw-bold">
                                Total Trekkers
                            </h6>
                            <h3>
                                {{ total_trekkers }}
                            </h3>
                        </div>
                    </div>
                </div>

            </div>

            <div class="card mb-5 mt-5">
                <div class="card-header">
                    <p class="mb-0 fw-bold">
                        Quick Actions
                    </p>
                </div>

                <div class="card-body">

                    <div class="row g-2">

                        <div class="col-md-3">
                            
                            <button @click = "emitCreateTrek" class="btn btn-primary w-100">
                                Create Trek
                            </button>

                        </div>

                        <div class="col-md-3">
                            
                            <button @click = "emitManageTrek" class="btn btn-success w-100">
                                Manage Treks
                            </button>

                        </div>

                        <div class="col-md-3">
                            <button @click = "emitBookings" class="btn btn-warning w-100">
                                Bookings
                            </button>
                        </div>

                        <div class="col-md-3">
                            <button @click="emitCreateStaff" class="btn btn-secondary w-100">

                                Create Staff

                            </button>
                        </div>

                    </div>

                </div>

                               
            </div>
            <div class= "card mb-5">
                    <div class = "card-header">
                        <p class = "fw-bold">
                            Recent Bookings
                        </p>
                    </div>
                    <div class="card-body">

                    <div class="table-responsive" style = "max-height: 250px; overflow-y: auto;">

                        <table class="table table-striped table-hover">

                            <thead>
                            <tr>
                                <th>Trek Name</th>
                                <th>Trekker Name</th>
                                <th>Booking Date</th>
                                <th>Start Date</th>
                                <th>End Date</th> 
                                <th>Booking Status</th>
                                <th>Trek Status</th>
                            </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "new_booking in filteredRrecentBookings" :key = "new_booking.booking_id">
                                    <td>{{ new_booking.trek_name }}</td>
                                    <td>{{ new_booking.trekker }}</td>
                                    <td>{{ formatDate(new_booking.booking_date) }}</td>
                                    <td>{{ formatDate(new_booking.start_date) }}</td>
                                    <td>{{ formatDate(new_booking.end_date) }}</td>
                                    
                                    <td v-if="new_booking.booking_status === 'Booked'">

                                        <span class="badge bg-success">
                                        {{ new_booking.booking_status }}
                                        </span>

                                    </td>
                                    <td v-else>

                                        <span class="badge bg-secondary">
                                        {{ new_booking.booking_status }}
                                        </span>

                                    </td>

                                
                                    <td v-if = "new_booking.trek_status === 'Open'">

                                        <span class="badge bg-success">
                                            {{ new_booking.trek_status }}
                                        </span>

                                    </td>
                                    <td v-else>

                                        <span class="badge bg-danger">
                                            {{ new_booking.trek_status }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>

                        </table>


                    </div>

                </div>
            </div> 
            <div class= "card mb-5">
                    <div class = "card-header">
                        <p class = "fw-bold">
                            Recent Treks
                        </p>
                    </div>
                    <div class="card-body">

                    <div class="table-responsive" style = "max-height: 250px; overflow-y: auto;">

                        <table class="table table-striped table-hover">

                            <thead>
                            <tr>
                                <th>Trek Name </th>
                                <th>Location</th>
                                <th>Duration</th>
                                <th>Status</th>
                                <th>Difficulty</th>
                                <th>Altitude</th>
                                <th>Price</th>

                            </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "new_trek in filteredRecentTreks" :key = "new_trek.trek_id">
                                    
                                    <td>{{ new_trek.trek_name }}</td>
                                    <td>{{ new_trek.location }}</td>
                                    <td>{{ new_trek.duration }}</td>
                                    <td v-if = "new_trek.status === 'Open'">

                                        <span class="badge bg-success">
                                            {{ new_trek.status }}
                                        </span>

                                    </td>
                                    <td v-else>

                                        <span class="badge bg-danger">
                                            {{ new_trek.status }}
                                        </span>
                                    </td>
                                    <td>{{ new_trek.difficulty }}</td>
                                    <td>{{ new_trek.altitude }}</td>
                                    <td>{{ formatCurrency(new_trek.price) }}</td>

                                </tr>
                            </tbody>

                        </table>
                        

                    </div>

                </div>
            </div> 


            

        </div>
    </div>

</div>

</template>


<script>
import TrekkerManagement from "@/components/admin/TrekkerManagement.vue";

import StaffManagement from "@/components/admin/StaffManagement.vue";

import CreateTrek from "@/components/admin/CreateTrek.vue";

import CreateStaff from "@/components/admin/CreateStaff.vue";

import TrekManagement from "@/components/admin/TrekManagement.vue";

import BookingManagement from "@/components/admin/BookingManagement.vue";


import axios from "axios";

export default {
    name: 'AdminDash',

    components: {
        TrekkerManagement,

        StaffManagement,

        CreateStaff,

        CreateTrek,

        TrekManagement,

        BookingManagement
    },

    data() {
        return {
            user: JSON.parse(localStorage.getItem('user')),

            total_treks: 0,
            active_treks: 0,
            total_bookings: 0,
            total_staff: 0,
            total_trekkers: 0,

            recent_treks : [],
            recent_bookings : [],

            searchText : ""
        };

        
    },


    computed : {
        filteredRrecentBookings() {
            const search = this.searchText.trim().toLowerCase();

            if (!search) {
                 return this.recent_bookings;
            }
            return this.recent_bookings.filter((booking) => {

                return [
                    // booking.booking_id,
                    booking.trek_name,
                    // booking.booking_date,
                    booking.trekker,
                    // booking.total_amount,
                    // booking.trek_status,
                    booking.assigned_staff,
                    // booking.trek_total_bookings,
                    // booking.trek_total_users_booked,
                    // booking.trek_total_amount
                ].join(" ").toLowerCase().includes(search);

            });
        },

        filteredRecentTreks() {

            const search = this.searchText.trim().toLowerCase();    

            if (!search) {

                return this.recent_treks;
            }

            return this.recent_treks.filter((trek) => {

                return [
                    trek.trek_name,
                    trek.location,
                    // trek.duration,
                    // trek.status,
                    // trek.difficulty,
                    // trek.altitude,
                    // trek.price
                ]
                    .join(" ")
                    .toLowerCase()
                    .includes(search);
            });
        }
    },


    mounted() {

        console.log("Mounted");

        this.fetchStats();

    },

    methods: {
        emitTrekker() {
            this.$emit('show-trekker');
        },

        emitTrekStaff() {
            this.$emit('show-staff');
        },

        emitCreateTrek() {
            this.$emit('show-trek');
        },

        emitManageTrek() {
            this.$emit('manage-trek');
        },


        logout() {
            localStorage.removeItem("user");
            this.$router.replace({ name: 'Login' });

        },

        async fetchStats() {
            try {
                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/dashboard", {
                    headers : {
                        "Authorization" : `Bearer ${token}`
                    }
                });

                if (res.status === 200) {
                    console.log(res.data);
                    this.total_treks = res.data.total_treks;
                    this.active_treks = res.data.active_treks;
                    this.total_bookings = res.data.total_bookings;
                    this.total_staff = res.data.total_staff;
                    this.total_trekkers = res.data.total_trekkers;
                    
                    this.recent_bookings = res.data.recent_bookings;
                    this.recent_treks = res.data.recent_treks;
                }
            } catch (error) {
                console.error("Error fetching dashboard stats:", error);
            }
        },


        emitCreateStaff() {
            this.$emit('create-staff');
        },

        emitBookings () {
            this.$emit('show-booking');
        },


        formatDate(dateValue) {

            if (!dateValue) return "-";

            return String(dateValue).slice(0, 10);

        },


        formatCurrency(amount) {
            return `₹${Number(amount || 0)}`;
        },


        emitReports() {
            this.$emit('show-reports');
        }


    },

    

}
</script>