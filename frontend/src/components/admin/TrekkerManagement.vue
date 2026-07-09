<template>
    <div class = "bg-light vh-100">
        
        
        <nav class = "navbar navbar-expand-lg bg-white border-bottom shadow-sm">

            <div class = "container-fluid px-3">
                <span class="navbar-brand fw-bold">
                    Trekkers Management
                </span>
                
                <div class="ms-auto">

                    <form class="d-flex">

                        <input v-model = "searchText" class="form-control me-2" type="search" placeholder="Search by name, email, or phone"   >
                        
                    </form>
                </div>
            </div>
        </nav>

        <div class = "container py-4">
            <div class  = "d-flex justify-content-between align-items-center mb-4">

                <div>

                    <h3 class="mb-2"> 
                        All Trekkers
                    </h3>
                    <small class="text-muted fw-semibold">Total: {{ filteredTrekkers.length }} Trekkers</small>

                </div>

            </div>

            <div class="card shadow-sm">

                <div class="card-header bg-white">
                    <strong>
                        Trekkers List
                    </strong>
                </div>

                <div class = "card-body">

                    <div class = "table-responsive">
                        
                        <table class="table table-hover align-middle">

                            <thead class="table-light">
                                <tr>
                                    <th>Trekker</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for="user in activeTrekkers" :key="user.id">
                                    <td>{{ user.name }}</td>
                                    <td>{{ user.email }}</td>
                                    <td>{{ user.phone }}</td>
                                    <td>

                                        <span class="badge bg-success">Active</span>

                                    </td>

                                    <td>
                                        <button @click = "deactivateUser(user.id)" class="btn btn-warning btn-sm me-2">

                                            Blacklist

                                        </button>

                                        <button @click = "deleteUser(user.id)" class="btn btn-danger btn-sm">
                                            Delete
                                        </button>
                                    </td>
                                </tr>

                                <tr v-if = "activeTrekkers.length === 0">

                                    <td colspan="5" class="text-center text-muted py-4">

                                        No trekkers found

                                    </td>

                                </tr>

                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <div class = "card shadow-sm mt-4">
                <div class = "card-header">
                    <strong>
                        Blacklisted Trekkers
                    </strong>
                </div>

                <div class = "card-body">
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Trekker</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Status</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for="user in blacklistedTrekkers" :key="user.id">
                                    <td>{{ user.name }}</td>
                                    <td>{{ user.email }}</td>
                                    <td>{{ user.phone }}</td>

                                    <td>
                                        <span class="badge bg-danger">Blacklisted</span>
                                    </td>

                                    <td>

                                        <button @click="activateUser(user.id)" class="btn btn-success btn-sm me-2">
                                            UnBlacklist
                                        </button>

                                        <button @click="deleteUser(user.id)" class="btn btn-danger btn-sm">
                                            Delete
                                        </button>

                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class = "d-flex justify-content-end mt-4 me-1" >
            <button class = "btn btn-secondary rounded-3 px-3" @click = "goBack">  
                    Go Back
                
            </button>
        </div>
        </div>
        
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'TrekkerManagement',

    data() {
        return {
            trekkers: [],
            searchText: ""
        }
    },

    computed: {
        filteredTrekkers() {

            const text = this.searchText.trim().toLowerCase();
            if (!text) {

                return this.trekkers;

            }


            return this.trekkers.filter(user => 

                user.name.toLowerCase().includes(text) ||
                user.email.toLowerCase().includes(text) ||
                user.phone.includes(text)

            );
        },

        activeTrekkers() {

            return this.filteredTrekkers.filter(user => Number(user.is_active) === 1);

        },
        blacklistedTrekkers() {

            return this.filteredTrekkers.filter(user => Number(user.is_active) === 0);

        }
    },

    mounted() {
        this.fetchTrekkers();
    },


    methods: {

        async fetchTrekkers() {

            try {

                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/all_trekkers", {

                    headers: {
                        "Authorization": `Bearer ${token}`
                    }

                });

                if (res.status === 200) {

                    this.trekkers = res.data.trekkers;
                    console.log("Trekkers loaded:", this.trekkers);

                }

            } catch (error) {

                console.error("Error fetching trekkers:", error);

            }
        },

        async deactivateUser(userId) {

            try {
                const token = localStorage.getItem("token");
                const res = await axios.post(`http://127.0.0.1:5000/api/admin/user_deactivate/${userId}`, {}, {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (res.status === 200) {
                    alert("Trekker deactivated successfully");
                    this.fetchTrekkers();
                }
            } catch (error) {
                console.error("Error deactivating trekker:", error);
                alert("Failed to deactivate trekker");
            }
        },

        async activateUser(userId) {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.post(`http://127.0.0.1:5000/api/admin/user_activate/${userId}`, {}, {
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }
                });

                if (res.status === 200) {
                    alert("Trekker activated successfully");
                    this.fetchTrekkers();
                }
            } catch (error) {
                console.error("Error activating trekker:", error);
                alert("Failed to activate trekker");
            }
        },

        async deleteUser(userId) {

            if (confirm("Are you sure you want to delete this trekker?")) {

                try {

                    const token = localStorage.getItem("token");

                    const res = await axios.post(`http://127.0.0.1:5000/api/admin/user_delete/${userId}`, {}, {

                        headers: {
                            "Authorization": `Bearer ${token}`

                        }
                    });

                    if (res.status === 200) {

                        alert("Trekker deleted successfully");
                        this.fetchTrekkers();
                        
                    }
                } catch (error) {

                    console.error("Error deleting trekker:", error);
                    alert("Failed to delete trekker");

                }
            }
        },

        goBack () {
            this.$emit('go-back');
        }
    }
}
</script>
