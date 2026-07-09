  
<template>
    <div class="container-fluid bg-light min-vh-100">

        <div class="row">

            <nav class="navbar navbar-expand-lg bg-light border-bottom px-2">
                <div class="container-fluid">

                    <span class="navbar-brand">
                        <h1 class="mt-2 fw-semibold display-4">
                            All Bookings
                        </h1>
                        <p class="fw-semibold text-muted ms-1">
                            View trek bookings and revenue
                        </p>
                    </span>

                    <div class="d-flex align-items-center gap-3">

                        <input v-model = "searchText" type= "search" class = "form-control" placeholder = "Search bookings..."  style="width: 280px">

                        <button @click = "goBack" class = "btn btn-secondary btn-lg px-4">
                            Go Back
                        </button>

                    </div>

                </div>
            </nav>
        </div>

        <div class="container py-4">

            <div class="row g-3 mb-4">

                <div class="col-md-6">

                    <div class="card shadow-sm border-0">
                        <div class="card-body">

                            <p class="text-muted fw-semibold mb-1">
                                Total Bookings With Open Treks
                            </p>

                            <h2 class="fw-bold mb-0">
                                {{ total_bookings }}
                            </h2>
                        </div>
                    </div>

                </div>

                <div class="col-md-6">
                    <div class="card shadow-sm border-0">
                        <div class="card-body">

                            <p class="text-muted fw-semibold mb-1">
                                Total Cancelled
                            </p>
                            <h2 class="fw-bold mb-0">
                                {{ cancelled_bookings }}
                            </h2>

                        </div>
                    </div>
                </div>
            </div>

            <div class="card shadow-sm border-0 mb-4">
                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        Bookings
                    </h4>
                    <p class="text-muted fw-semibold mb-0">
                        All trek booking records
                    </p>
                </div>

                <div class="card-body">

                    <div v-if = "filteredBookings.length === 0" class="text-muted">
                        No bookings found.
                    </div>

                    <div v-else class="table-responsive">

                        <table class="table table-hover table-striped align-middle">
                            
                            <thead>
                                <tr>
                                    <th>Booking ID</th>
                                    <th>Trek Name</th>
                                    <th>Trekker Name</th>
                                    <th>Booking Date</th>
                                    <th>Total Amount</th>
                                    <th>Trek Status</th>
                                    <th>Booking Status</th>
                                    <th>Assigned Staff</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for = "booking in filteredBookings" :key="booking.booking_id">

                                    <td>{{ booking.booking_id }}</td>

                                    <td>{{ booking.trek_name }}</td>

                                    <td>{{ formatDate(booking.booking_date) }}</td>

                                    <td>{{ booking.trekker }}</td>

                                    <td>{{ formatCurrency(booking.total_amount) }}</td>

                                    <td v-if = "booking.trek_status === 'Open'">
                                        <span class="badge bg-success">
                                            {{ booking.trek_status }}
                                        </span>
                                    </td>

                                    <td v-else>
                                        <span class="badge bg-danger">
                                            {{ booking.trek_status }}
                                        </span>
                                    </td>

                                    <td v-if = "booking.booking_status === 'Booked'">
                                        <span class="badge bg-success">
                                            {{ booking.booking_status }}
                                        </span>
                                    </td>

                                    <td v-else>
                                        <span class="badge bg-danger">
                                            {{ booking.booking_status }}
                                        </span>
                                    </td>

                                    <td>{{ booking.assigned_staff || "Not assigned" }}</td>

                                </tr>
                            </tbody>

                        </table>

                    </div>
                </div>
            </div>


            <div class="card shadow-sm border-0 mb-5">

                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        Trek Booking Summary
                    </h4>
                    <p class="text-muted fw-semibold mb-0">
                        Active bookings, participants, and amount by trek
                    </p>

                </div>


                <div class = "card-body">

                    <div v-if = "filteredBookings.length === 0" class = "text-muted">

                        No trek summary available.

                    </div>

                    <div v-else class = "table-responsive">

                        <table class="table table-hover table-striped align-middle">

                            <thead>

                                <tr>
                                    <th>Trek Name</th>
                                    <th>Total Active Bookings</th>
                                    <th>Total Participants</th>
                                    <th>Total Amount</th>
                                </tr>

                            </thead>

                            <tbody>

                                <tr v-for = "booking in filteredBookings" :key="booking.booking_id">

                                    <td>{{ booking.trek_name }}</td>

                                    <td>{{ booking.trek_total_bookings }}</td>

                                    <td>{{ booking.trek_total_users_booked }}</td>

                                    <td>{{ formatCurrency(booking.trek_total_amount) }}</td>

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

export default {

    name: "BookingManagement",


    data() {
        return {

            searchText: "",
            bookings: [],
            total_bookings: 0,
            cancelled_bookings: 0

        };

    },



    computed: {

        filteredBookings() {                                  // filteredBookings depends on bookings
            const search = this.searchText.trim().toLowerCase();
            if (!search) {
                return this.bookings;          // since this.bookings changed in fetchBookings() vue automatically reacalculates filteredBookings and so now vue renders whatever filteredBookings returns.
            }
            return this.bookings.filter((booking) => {
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
                ]
                    .join(" ")
                    .toLowerCase()
                    .includes(search);

            });

        },


    },





    mounted() {
        this.fetchBookings();
    },





    methods: {


        goBack() {
            this.$emit("go-back");
        },


        async fetchBookings() {

            try {

                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/bookings",

                {
                    headers: {

                        Authorization: `Bearer ${token}`

                    }

                });

                if (res.status === 200) {

                    this.bookings = res.data.bookings || [];
                    this.total_bookings = res.data.total_bookings || 0;
                    this.cancelled_bookings = res.data.cancelled_bookings || 0;

                }

            } catch (error) {

                console.error("Error fetching bookings:", error);
                alert("Could not fetch bookings.");
            }
        },


        formatDate(dateValue) {

            if (!dateValue) return "-";

            return String(dateValue).slice(0, 10);

        },


        formatCurrency(amount) {

            return `₹${Number(amount || 0)}`;
        },
       
    }
};
</script>
