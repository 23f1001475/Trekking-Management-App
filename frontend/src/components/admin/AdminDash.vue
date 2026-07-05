
<template>
<div class="container-fluid bg-light vh-100">
    <div class = "row">
        <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm px-3">
            <div class="container-fluid">

                <span class="navbar-brand">
                    Welcome {{ user.username }}
                </span>

                <div class="d-flex align-items-center">
                    <button @click = "emitTrekker" class = "btn btn-transparent fw-semibold me-2"> Trekkers </button>
                    <button @click = "emitTrekStaff" class = "btn btn-transparent fw-semibold me-3"> Trek Staff </button>

                    <form class="d-flex me-3">
                        <input
                            class="form-control me-2"
                            type="search"
                            placeholder="Search"
                        >
                        <button class="btn btn-outline-success">
                            Search
                        </button>
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
                            <a href="/admin/create_trek" class="btn btn-primary w-100">
                                Create Trek
                            </a>
                        </div>

                        <div class="col-md-3">
                            <a href="/admin/all_treks" class="btn btn-success w-100">
                                Manage Treks
                            </a>
                        </div>

                        <div class="col-md-3">
                            <a href="/admin/bookings" class="btn btn-warning w-100">
                                Bookings
                            </a>
                        </div>

                        <div class="col-md-3">
                            <a href="/admin/create_staff" class="btn btn-secondary w-100">
                                Create Staff
                            </a>
                        </div>

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

                    <div class="table-responsive">

                        <table class="table table-striped table-hover">

                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Trekker</th>
                                <th>Trek</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                            </thead>

                            <tbody id="bookingTable">
                                <tr>
                                    <td>1</td>
                                    <td>John Doe</td>
                                    <td>Mount Everest</td>
                                    <td>2023-06-01</td>
                                    <td>Confirmed</td>
                                </tr>
                            </tbody>

                        </table>


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

                    <div class="table-responsive">

                        <table class="table table-striped table-hover">

                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Trekker</th>
                                <th>Trek</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                            </thead>

                            <tbody id="bookingTable">
                                <tr>
                                    <td>1</td>
                                    <td>John Doe</td>
                                    <td>Mount Everest</td>
                                    <td>2023-06-01</td>
                                    <td>Confirmed</td>
                                </tr>
                            </tbody>

                        </table>
                        

                    </div>

                </div>
            </div> 

            <div class="card">

                <div class="card-header">
                    <strong>Recent Bookings</strong>
                </div>

                <div class="card-body">

                    <div class="table-responsive">

                        <table class="table table-striped table-hover">

                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Trekker</th>
                                <th>Trek</th>
                                <th>Date</th>
                                <th>Status</th>
                            </tr>
                            </thead>

                            <tbody id="bookingTable">
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

import axios from "axios";
export default {
    name: 'AdminDash',

    components: {
        TrekkerManagement,

        StaffManagement
    },

    data() {
        return {
            user: JSON.parse(localStorage.getItem('user')),

            total_treks: 0,
            active_treks: 0,
            total_bookings: 0,
            total_staff: 0,
            total_trekkers: 0
        };

        
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
                }
            } catch (error) {
                console.error("Error fetching dashboard stats:", error);
            }
        }

    },

    

}
</script>