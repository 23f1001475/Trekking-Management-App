<template>
    <div class = "container-fluid  bg-light vh-100">
        <div>
            <div class = "row">
                <nav class="navbar navbar-expand-lg bg-white border-bottom shadow-sm px-2">
                    <div class="container-fluid">
                    <span class = "navbar-brand">
                        <strong>
                            Staff Management
                        </strong>
                    </span>

                    <div class = "d-flex align-items-end">

                        <button @click = "emitTrekker" class = "btn btn-transparent fw-semibold me-2"> Trekkers </button>

                        <form class = "d-flex me-3">
                            <input v-model = "searchText" class = "form-control me-2"  type="search"  placeholder = "Search" >
                            
                        </form>

                        <button @click="logout()" class="btn btn-secondary">
                            Logout
                        </button>
                    </div>
                    </div>
                </nav>

            </div>

            <div class = "container-fluid mt-3">

                <div>
                    <h3 class="mb-2">All Staffs</h3>
                    <small class="text-muted fw-semibold">Total: {{ filteredStaffs.length }} Staffs</small>
                </div>

                <div class = "card shadow-sm mt-3 mb-3">
                    <div class = "card-header">
                        <strong>
                            Staff
                        </strong>
                    </div>
                    <div class = "card-body">
                        <div class = table-responsive>
                        <table class = "table table-hover table-striped table-bordered">
                            <thead>
                                <tr>
                                    <th>
                                        Name
                                    </th>
                                    <th>
                                        Email
                                    </th>
                                    <th>
                                        Phone
                                    </th>
                                    <th>
                                        Status
                                    </th>
                                    <th class = "text-center">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for = "staff in activeStaffs" :key = "staff.id">
                                    <td>
                                        {{ staff.name }}
                                    </td>
                                    <td>
                                        {{ staff.email }}
                                    </td>
                                    <td>
                                        {{ staff.phone }}
                                    </td>
                                    
                                    <td>
                                        <span class="badge bg-success">Active</span>
                                    </td>

                                    <td class = "text-center">
                                        <button @click = "deactivateUser(staff.id)" class = "btn btn-sm btn-primary me-2">
                                            Blacklist
                                        </button>
                                        <button @click = "deleteStaff(staff.id)" class = "btn btn-sm btn-danger">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        </div>

                        <div>
                            <button @click = "emitCreateStaff" class = "btn btn-primary">
                                Add Staff
                            </button>
                        </div>
                    </div>

                </div>

                <div class = "card shadow-sm">
                    <div class = "card-header">
                        <strong>
                            Blacklisted Staff
                        </strong>     
                    </div>

                    <div class = "card-body">
                        <div class = table-responsive>
                        <table class = "table table-hover table-striped table-bordered">
                            <thead>
                                <tr>
                                    <th>
                                        Name
                                    </th>
                                    <th>
                                        Email
                                    </th>
                                    <th>
                                        Phone
                                    </th>
                                    <th>
                                        Status
                                    </th>
                                    <th class = "text-center">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for = "staff in blacklistedStaffs" :key = "staff.id">
                                    <td>
                                        {{ staff.name }}
                                    </td>

                                    <td>
                                        {{ staff.email }}
                                    </td>

                                    <td>
                                        {{ staff.phone }}
                                    </td>

                                    <td>
                                        <span class="badge bg-danger">Blacklisted</span>
                                    </td>

                                    <td class = "text-center">
                                        <button @click = "activateUser(staff.id)" class = "btn btn-sm btn-success me-2">
                                            Unblacklist
                                        </button>
                                        <button @click = "deleteStaff(staff.id)" class = "btn btn-sm btn-danger">
                                            Delete
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        </div>
                    </div>
                                

                </div>
                
                <div class = "mt-4 me-1" style = "display : flex; justify-content : end">

                    <button @click = "goBack()" class = "btn btn-secondary">
                         Go Back 
                    </button>
                </div>

            </div>
        
                                

        </div>
        
     
    </div>
</template>





<script>

import axios from "axios";

export default {
    name: "StaffManagement",


    data () {
        return {
            staff : [],
            searchText : ""
        }
    },


    computed : {

        filteredStaffs() {

            const text = this.searchText.trim().toLowerCase();
            if (!text) {
                return this.staff;
            }

            return this.staff.filter(staff => 
                staff.name.toLowerCase().includes(text) ||
                staff.email.toLowerCase().includes(text) ||
                staff.phone.includes(text)
            );
        },



        activeStaffs () {
            return this.filteredStaffs.filter(user => Number(user.is_active) === 1);
        },


        blacklistedStaffs () {
            return this.filteredStaffs.filter(user => Number(user.is_active) === 0);
        }
    },

    mounted() {
        this.fetchstaffs();
    },

    methods : {

        async fetchstaffs() {
            try {
                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/all_staffs", {
                    
                    headers: {
                        "Authorization": `Bearer ${token}`
                    }

                });

                if (res.status === 200) {

                    this.staff = res.data.staffs;

                    console.log("Staffs loaded:", this.staff);
                }

            } catch (error) {
                console.error("Error fetching staffs:", error);
            }
        },

        async activateUser (userId) {
            try {   
                const token = localStorage.getItem("token");

                const res = await axios.post(`http://127.0.0.1:5000/api/admin/user_activate/${userId}`, {}, {
                    
                    headers: {

                        "Authorization": `Bearer ${token}`

                    }

                });

                if (res.status === 200) {

                    alert("Trekker activated successfully");

                    this.fetchstaffs();
                }

            } catch (error) {
                console.error("Error activating trekker:", error);

                alert("Failed to activate trekker");
            }
        },


        async deactivateUser (userId) {
            try {   
                const token = localStorage.getItem("token");

                const res = await axios.post(`http://127.0.0.1:5000/api/admin/user_deactivate/${userId}`, {}, {
                    
                    headers: {

                        "Authorization": `Bearer ${token}`

                    }

                });

                if (res.status === 200) {                    

                    alert("Trekker deactivated successfully");

                    this.fetchstaffs();
                }

            } catch (error) {
                console.error("Error deactivating trekker:", error);

                alert("Failed to deactivate trekker");
            }
        },

        async deleteStaff (userId) {
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

                        this.fetchstaffs();
                    }

                } catch (error) {
                    console.error("Error deleting trekker:", error);

                    alert("Failed to delete trekker");
                }
            }
        },



        goBack () {
            this.$emit('go-back');
        },

        emitTrekker() {
            this.$emit('show-trekker');
        },

        logout() {
            localStorage.removeItem("user");
            this.$router.replace({ name: 'Login' });

        },

        emitCreateStaff() {
            this.$emit('create-staff');
        }
    }
}




</script>