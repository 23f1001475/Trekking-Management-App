<template>
    <div class = "container-fluid bg-light min-vh-100">
        <div class = "bg-light ">
            <div class = "row">
                <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm">
                    <div class = "container-fluid">
                        <span class = "navbar-brand">
                            <div class ="fw-semibold display-4">
                            Trek History
                            </div>
                        </span>
                        
                        
                        <div class = "d-flex align-items-center gap-3">
                            <input v-model = "searchText"   class = "form-control w-auto" type = "search" placeholder = "Search" >

                            <button @click = "goBack()" class = "btn btn-secondary">
                                Go Back
                            </button>
                        </div>
                    </div>
                    
                </nav>
            </div>

            <div class = "container">

                <div class ="card shadow-sm mt-5 border-0">

                    <div class = "card-header border-bottom">

                           <div class = "fw-semibold">
                               Trek History
                            </div> 
         
                    </div>

                    <div class = "card-body">
                        <table class = "table table-hover table-responsive table-bordered table-striped">
                            <thead>
                                <tr>
                                    <th>
                                        Trek Name
                                    </th>
                                    <th>
                                        Booking Date
                                    </th>
                                    <th>
                                        End Date
                                    </th>
                                    <th>
                                        Price
                                    </th>
                                    <th>
                                        Status
                                    </th>
                                    
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for="history in filteredHistory" :key = "history.booking_id">

                                    <td> {{ history.trek_name }}</td>
                                    <td> {{ formatDate(history.booking_date) }}</td>
                                    <td> {{ formatDate(history.end_date) }}</td>
                                    <td> {{ history.price }}</td>
                                    <td> {{ history.status }}</td>
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


import axios from "axios"
export default {
    name: "TrekHistory",

    data() {
        return {
            history_data : [],
            searchText : ""
        }
    },

    computed: {

        filteredHistory() {

            const search = this.searchText.trim().toLowerCase();
            if (!search) {

                return this.history_data;

            }
            return this.history_data.filter((history) => {

                return history.trek_name.toLowerCase().includes(search);

            });
        }

    },

    mounted() {
        this.fetchHistory()
    },

    methods: {

        async fetchHistory() {

        try{

            const token = localStorage.getItem("token");

            const res = await axios.get('http://127.0.0.1:5000/api/trekkers/history', {

                headers:{
                    "Authorization" : `Bearer ${token}`

                }
        });
        if (res.status === 200) {

            this.history_data = res.data.history_data;
            console.log(this.history_data);
        }
        

        } catch (error){

            console.error("Error fetching trek history:", error);
        };

        },


        goBack() {
            this.$emit("go-back");
        },


        formatDate(dateValue) {

            return String(dateValue).slice(0, 10);
            
        }

        
    }


}
</script>