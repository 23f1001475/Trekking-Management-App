<template>
    
    <div class = "container-fluid vh-min-100 bg-light">

        <div class = "row">

            <nav class = "navbar bg-white border-bottom shadow-sm px-3">
                <div class = "container-fluid">
                    <span class = "navbar-brand">
                        <div class = "fw-semibold display-3">
                            Reports
                        </div>
                    </span>
                    
                    <div class = "d-flex">
                        <input  v-model = "searchText" class = "form-control me-2" type = "search" placeholder = "Search" aria-label = "Search" style = "width: 180px">
                        <button @click = "goBack()" class = "btn btn-secondary">
                            Go Back
                        </button>
                    </div>
                </div>

            </nav>

        </div>

        <div class = "container" >
            <div>
            <div class = "card shadow-sm mt-5 rounded-4 ">

                <div class = "card-header">

                    <div class = "text-center">
                        <strong>
                            Quick Summary
                        </strong>
                    </div>

                </div>

                <div class = "card-body p-4">

                    <div class = "row">
                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">

                                <div class = "card-header border-0 rounded-top-5 text-center">

                                    <strong>
                                        Total Trek Routes
                                    </strong>

                                </div>
                                <div class = "card-body text-center">

                                    <h1>
                                        {{ total_treks_routes }}
                                    </h1>

                                </div>

                            </div>
                        </div>

                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">
                                <div class = "card-header border-0 rounded-top-5 text-center">
                                    <strong>
                                        Scheduled Routes
                                    </strong>
                                </div>
                                <div class = "card-body  text-center" >
                                    <h1>
                                        {{ total_scheduled_treks }}
                                    </h1>
                                </div>
                            </div>
                        </div>

                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">
                                <div class = "card-header border-0 rounded-top-5 text-center">
                                    <strong>
                                        Total Trekkers
                                    </strong>
                                </div>
                                <div class = "card-body  text-center">
                                    <h1>
                                        {{ total_trekkers }}
                                    </h1>
                                </div>
                            </div>
                        </div>

                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">
                                <div class = "card-header border-0 rounded-top-5 text-center">
                                    <strong>
                                        Total Trek Staffs
                                    </strong>
                                </div>
                                <div class = "card-body  text-center">
                                    <h1>
                                        {{ total_staffs }}
                                    </h1>
                                </div>
                            </div>
                        </div>

                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">
                                <div class = "card-header border-0 rounded-top-5 text-center">
                                    <strong>
                                        Total Bookings
                                    </strong>
                                </div>
                                <div class = "card-body  text-center">
                                    <h1>
                                        {{ total_bookings }}
                                    </h1>
                                </div>
                            </div>
                        </div>

                        <div class = "col-2">
                            <div class = "card shadow-sm border-0 rounded-5">
                                <div class = "card-header border-0 rounded-top-5 text-center">
                                    <strong>
                                        total Revenue
                                    </strong>
                                </div>
                                <div class = "card-body  text-center">
                                    <h1>
                                        {{ formatCurrency(total_revenue) }}
                                    </h1>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>


            <div class = "card shadow-sm mt-5 rounded-4">

                <div class = "card-header">

                    <div class = "text-center">
                        <strong>
                            Most Popular Treks
                        </strong>
                        <p class = "text-muted">
                            Treks with most number of bookings
                        </p>
                    </div>

                </div>

                <div class = "card-body p-4">

                    <div class = "table-responsive  rounded-4 border">
                        <table class = "table table-hover table-bordered table-striped" style = "border-radius: 20px;">
                            
                            <thead>
                                <tr class = "text-center">
                                    <th>
                                        Trek Name
                                    </th>
                                    <th>
                                        Number of Bookings
                                    </th>
                                </tr>

                            </thead>

                            <tbody>
                                <tr v-for="popular_trek in filteredTrekRoute" :key = "popular_trek.id"  class = "text-center">
                                    <td>
                                        {{ popular_trek.route_name }}
                                    </td>
                                    <td>
                                        {{ popular_trek.total_bookings }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    

                    
                </div>


                
            </div>



            <div class = "card shadow-sm mt-5 rounded-4">

                <div class = "card-header">

                    <div class = "text-center">
                        <strong>
                            Most Active Trek Staff
                        </strong>
                        <p class = "text-muted">
                            Trek staff with most number of treks assigned
                        </p>
                    </div>

                </div>

                <div class = "card-body p-4">

                    <div class = "table-responsive  rounded-4 border">
                        <table class = "table table-hover table-bordered table-striped" style = "border-radius: 20px;">
                            
                            <thead>
                                <tr class = "text-center">
                                    <th>
                                        Staff Name
                                    </th>
                                    <th>
                                        Treks Assigned
                                    </th>
                                </tr>
                            </thead>


                            <tbody>
                                <tr v-for="staff in filteredTrekStaff" :key = "staff.id" class = "text-center">
                                    <td>
                                        {{ staff.name }}
                                    </td>
                                    <td>
                                        {{ staff.total_assigned_treks }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    

                    
                </div>


                
            </div>




            <div class = "card shadow-sm mt-5 rounded-4">

                <div class = "card-header">

                    <div class = "text-center">
                        <strong>
                            Revenue Summary
                        </strong>
                        <p class = "text-muted">

                            Treks with highest revenue generated

                        </p>
                    </div>

                </div>

                <div class = "card-body p-4">

                    <div class = "table-responsive  rounded-4 border">
                        <table class = "table table-hover table-bordered table-striped" style = "border-radius: 20px;">
                           
                            <thead>
                                <tr class = "text-center">
                                    <th>
                                        Trek Name
                                    </th>
                                    <th>
                                        Total Revenue
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for="trek in filteredTrekRevenue" :key = "trek.id" class = "text-center">
                                    <td>
                                        {{ trek.trek_name }}
                                    </td>
                                    <td>
                                        {{ formatCurrency(trek.total_trek_revenue) }}
                                    </td>
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

import axios from "axios";
export default {
    name: "Reports",

    data() {
        return {
            searchText : "",

            total_treks_routes : 0,
            total_scheduled_treks : 0,
            total_trekkers : 0,
            total_staffs : 0,
            total_bookings : 0,
            total_revenue : 0,

            result_trek_revenue : [],
            result_trek_routes : [],
            result_trek_staffs : []
            
        }
    },


    computed : {

        filteredTrekRevenue() {
            const search = this.searchText.trim().toLowerCase();
            if (!search) {
                return this.result_trek_revenue;
            }
            return this.result_trek_revenue.filter((report) => {

                return report.trek_name.toLowerCase().includes(search);

            });
        },

        filteredTrekRoute(){
            const search = this.searchText.trim().toLowerCase();
            if (!search) {
                return this.result_trek_routes;
            }
            return this.result_trek_routes.filter((report) => {

                return report.route_name.toLowerCase().includes(search);

            });
        },

        filteredTrekStaff() {
            const search = this.searchText.trim().toLowerCase();
            if (!search) {
                return this.result_trek_staffs;
            }
            return this.result_trek_staffs.filter((report) => {                

                return report.name.toLowerCase().includes(search);

            });
        }
        
    },


    mounted () {
        this.fetchReports();
    },


    methods: {
        goBack() {
            this.$emit("go-back");
        },


        async fetchReports() {

            try {

                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/reports", {

                    headers: {
                        
                        "Authorization" : `Bearer ${token}`
                         }
                });

                if (res.status === 200) {
                    
                    console.log(res.data);
                    this.total_treks_routes = res.data.total_treks_routes;
                    this.total_scheduled_treks = res.data.total_scheduled_treks;
                    this.total_trekkers = res.data.total_trekkers;
                    this.total_staffs = res.data.total_staffs;
                    this.total_bookings = res.data.total_bookings;
                    this.total_revenue = res.data.total_revenue;
                    this.result_trek_routes = res.data.result_trek_routes;
                    this.result_trek_staffs = res.data.result_trek_staffs;
                    this.result_trek_revenue = res.data.result_trek_revenue; 
                }       

            } catch (error) {

                console.error("Error fetching reports:", error);
            }
        },

        formatCurrency(amount) {
            return `₹${Number(amount || 0)}`;
        }
    }
}
</script>