<!-- <template>

    <div>  

        <h1>Manage Scheduled Treks</h1>

    </div>

    <div>
        <button @click = "goBack()" class = "btn btn-secondary">
            Go Back
        </button>
    </div>

</template>

<script>
export default {
    name: "ManageScheduledTrek",

    methods: {
        goBack() {
            this.$emit("go-back");
        }
    }
};
</script> -->


<!-- <template>
    <div class="container-fluid bg-light vh-100">
  
        <div class="row">
            <nav class="navbar navbar-expand-lg bg-light border-bottom px-2">
                <div class="container-fluid">

                    <span class="navbar-brand">
                        <h1 class="mt-2 fw-semibold display-4">
                            Manage Trek
                        </h1>
                        <p class="fw-semibold text-muted ms-1">
                            Edit trek details, assign or remove staff
                        </p>
                    </span>

                    <div class="d-flex align-items-end">
                        <button @click = "goBack" class = "btn btn-secondary btn-lg px-4">
                            Go Back
                        </button>
                    </div>
                </div>
            </nav>
        </div>
  
        <div class="container py-4">
  
            <div class="card shadow-sm border-0 mb-4">

                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        Trek Details
                    </h4>
                    <p class="text-muted fw-semibold mb-0">
                        Update the scheduled trek information
                    </p>

                </div>

                <div class="card-body">
                      
                    <form @submit.prevent = "handleSaveTrek">

                        <div class="row g-3" >
                            <div class="col-md-6">

                                <label class="form-label fw-semibold">
                                    Trek Name
                                </label>

                                <input v-model = "form.trek_name" type = "text" class = "form-control" placeholder = "Trek Name">
                                
                                <p v-for = "error in errors.trek_name" :key="error" class = "text-danger small mt-1">
                                    {{ error }}
                                </p>

                            </div>
                            
                            <div class = "col-md-3">
                                <label class = "form-label fw-semibold">
                                    
                                    Start Date
                                
                                </label>
                                 
                                <input v-model = "form.start_date" type = "date" class = "form-control">
                                <p v-for = "error in errors.start_date" :key = "error" class = "text-danger small mt-1">
                                    
                                    {{ error }}
                                
                                </p>
                                </div>
                                <div class = "col-md-3">
                                     
                                    <label class = "form-label fw-semibold">
                                        End Date
                                    </label>
                                
                                    <input v-model = "form.end_date" type = "date" class = "form-control">
                                    
                                    <p v-for = "error in errors.end_date" :key = "error" class= "text-danger small  mt-1">
                                        {{ error }}
                                    </p>
                                </div>
                               
                                <div class = "col-md-3">

                                    <label class="form-label fw-semibold">
                                        Total Slots
                                    </label>

                                    <input v-model = "form.total_slots" type = "number" class = "form-control" placeholder="Total Slots">
                                        
                                    <p v-for = "error in errors.total_slots" :key = "error" class = "text-danger small mt-1">
                                        {{ error }}
                                    </p>
                                </div>
                                
                                <div class="col-md-3">
                                    
                                    <label class="form-label fw-semibold">
                                        Available Slots
                                    </label>
                                    
                                    <input v-model="form.available_slots" type="number" class="form-control" placeholder="Available Slots">
                                    
                                    <p v-for = "error in errors.available_slots" :key = "error" class = "text-danger small mt-1">
                                        
                                        {{ error }}
                                    
                                    </p>
                                </div>
                                
                                <div class = " col-md-3">
                                    <label class="form-label fw-semibold">
                                        
                                        Price
                                    
                                    </label>
                                    <input v-model = "form.price" type = "number" class = "form-control" placeholder="Price">
                                    
                                    <p v-for = "error in errors.price" :key = "error" class = "text-danger small mt-1">{{ error }}</p>
                                </div>
                              
                                <div class = "col-md-3">
                                    
                                    <label class="form-label fw-semibold">
                                        Status
                                    
                                    </label>

                                    <select v-model = "form.status" class = "form-select">

                                        <option value="Open">Open</option>
                                        <option value="Closed">Closed</option>
                                        <option value="Cancelled">Cancelled</option>
                                        <option value="Completed">Completed</option>

                                    </select>
                                    
                                    <p v-for = "error in errors.status" :key = "error" class = "text-danger small mt-1">{{ error }}</p>
                                </div>
                            </div>

                            <div class = "mt-4">

                                <button type = "submit" class = "btn btn-success px-5 fw-semibold">
                                    Save Changes
                                </button>

                            </div>
                        </form>
                    </div>
                </div>
  

            <div class = "card shadow-sm border-0 mb-4">

                <div class = "card-header bg-white border-bottom">

                    <h4 class = "fw-semibold mb-0">
                        
                        Assigned Staff
                    </h4>
                    
                    <p class="text-muted fw-semibold mb-0">
                        
                        Staff currently assigned to this trek
                    
                    </p>
                </div>
                
                <div class = "card-body">
                    <div v-if = "assigned_staff.length === 0" class = "text-muted">
                        
                        No staff assigned to this trek yet.

                    </div>

                    <table v-else class = "table table-hover table-striped">
                        
                        <thead>

                            <tr>
                                <th>
                                    Staff Name
                                </th>
                                <th>
                                    Email
                                </th>
                                <th>
                                    Phone
                                </th>
                                <th class = "text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        
                        <tbody>
                            <tr v-for = "staff in assigned_staff" :key = "staff.assignment_id">
                                  
                                <td>
                                    {{ staff.staff_name }}
                                </td>

                                <td>
                                    {{ staff.staff_email }}
                                </td>

                                <td>
                                    {{ staff.staff_phone }}
                                </td>

                                <td class = "text-center">

                                    <button @click = "handleRemoveStaff(staff.assignment_id)" class = "btn btn-sm btn-outline-danger px-3">
                                        Remove
                                    </button>

                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>


  
            <div class="card shadow-sm border-0 mb-4">
                
                <div class="card-header bg-white border-bottom">
                    
                    <h4 class = "fw-semibold mb-0">
                        Available Staff
                    </h4>
                    
                    <p class="text-muted fw-semibold mb-0">
                        Select staff to assign to this trek
                    </p>
                </div>
                
                <div class="card-body">
                    
                    <div v-if = "all_staff.length === 0" class = "text-muted">
                        
                        No staff available.

                    </div>
                    
                    <table v-else class = "table table-hover table-striped">
                        
                        <thead>
                            
                            <tr>
                                <th>
                                    Staff Name
                                </th>
                                <th>
                                    Email
                                </th>
                                <th>
                                    Phone
                                </th>
                                <th class="text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        
                        <tbody>
                            <tr v-for = "staff in all_staff" :key = "staff.id">
                                <td>
                                    {{ staff.name }}
                                </td>
                                <td>
                                    {{ staff.email }}
                                </td>
                                <td>
                                    {{ staff.phone }}
                                </td>
                                <td class="text-center">
                                    
                                    <button @click = "handleAssignStaff(staff.id)" class = "btn btn-sm btn-outline-success px-3" :disabled = "isAlreadyAssigned(staff.id)">
                                            
                                        {{ isAlreadyAssigned(staff.id) ? 'Assigned' : 'Add Staff' }}

                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
  
            

            <div class = "card shadow-sm border-0 border-danger mb-5">
                
                <div class = "card-header bg-white border-bottom border-danger">
                    
                    <h4 class = "fw-semibold text-danger mb-0">
                        
                        Danger Zone
                    
                    </h4>
                
                </div>
            
                <div class="card-body d-flex align-items-center justify-content-between">
                    
                    <div>
                        
                        <p class="fw-semibold mb-0">
                            Delete this trek
                        </p>
                        
                        <p class="text-muted small mb-0">
                            
                            This action is permanent and cannot be undone.
                        
                        </p>
                    </div>
                    
                    <button @click = "handleDeleteTrek" class = "btn btn-danger px-5 fw-semibold">
                        
                        Delete Trek
                    
                    </button>
                </div>
            </div>
  
        </div>
    </div>
</template>
  
  <script>
  import axios from "axios";
  
  export default {
      name: "ManageScheduledTrek",
  
      props: {
          trekId: {
              type: Number,
              required: true
          }
      },
  
      data() {
          return {
              form: {
                  trek_name: "",
                  start_date: "",
                  end_date: "",
                  total_slots: "",
                  available_slots: "",
                  price: "",
                  status: "Open"
              },
              errors: {},
              assigned_staff: [],
              all_staff: []
          };
      },
  
      mounted() {
          this.fetchTrekDetails();
          this.fetchAssignedStaff();
          this.fetchAllStaff();
      },
  
      methods: {
          goBack() {
              this.$emit("go-back");
          },
  
          async fetchTrekDetails() {
              try {
                  const token = localStorage.getItem("token");
  const res = await
  axios.get(`http://127.0.0.1:5000/api/admin/scheduled_trek/${this.trekId}`, {
                      headers: { Authorization: `Bearer ${token}` }
                  });
                  if (res.status === 200) {
                      const t = res.data.trek;
                      this.form.trek_name = t.trek_name;
                      this.form.start_date = t.start_date;
                      this.form.end_date = t.end_date;
                      this.form.total_slots = t.total_slots;
                      this.form.available_slots = t.available_slots;
                      this.form.price = t.price;
                      this.form.status = t.status;
                  }
              } catch (error) {
                  console.error("Error fetching trek details:", error);
              }
          },
  
          async fetchAssignedStaff() {
              try {
                  const token = localStorage.getItem("token");
  const res = await
  axios.get(`http://127.0.0.1:5000/api/admin/treks/${this.trekId}/staff`, {
                      headers: { Authorization: `Bearer ${token}` }
                  });
                  if (res.status === 200) {
                      this.assigned_staff = res.data.assigned_staff;
                  }
              } catch (error) {
                  console.error("Error fetching assigned staff:", error);
              }
          },
  
          async fetchAllStaff() {
              try {
                  const token = localStorage.getItem("token");
  const res = await axios.get("http://127.0.0.1:5000/api/admin/all_staffs", {
                      headers: { Authorization: `Bearer ${token}` }
                  });
                  if (res.status === 200) {
                      this.all_staff = res.data.staffs;
                  }
              } catch (error) {
                  console.error("Error fetching all staff:", error);
              }
          },
  
          async handleSaveTrek() {
              this.errors = {};
              try {
                  const token = localStorage.getItem("token");
                  const res = await axios.put(
  `http://127.0.0.1:5000/api/admin/scheduled_treks/${this.trekId}/update_trek`,
                      this.form,
                      { headers: { Authorization: `Bearer ${token}` } }
                  );
                  if (res.status === 200) {
                      alert("Trek updated successfully");
                  }
              } catch (error) {
                  if (error.response && error.response.status === 400) {
                      this.errors = error.response.data.errors || {};
                  } else {
                      alert("Something went wrong while saving.");
                  }
              }
          },
  
          async handleAssignStaff(staffId) {
              try {
                  const token = localStorage.getItem("token");
                  const res = await axios.post(
  `http://127.0.0.1:5000/api/admin/treks/${this.trekId}/assign_staff`,
                      { staff_id: staffId },
                      { headers: { Authorization: `Bearer ${token}` } }
                  );
                  if (res.status === 200) {
                      await this.fetchAssignedStaff();
                  }
              } catch (error) {
                  console.error("Error assigning staff:", error);
                  alert("Could not assign staff.");
              }
          },
  
          async handleRemoveStaff(assignmentId) {
              try {
                  const token = localStorage.getItem("token");
                  const res = await axios.post(
  `http://127.0.0.1:5000/api/admin/assignments/${assignmentId}`,
                      { trek_id: this.trekId },
                      { headers: { Authorization: `Bearer ${token}` } }
                  );
                  if (res.status === 200) {
                      await this.fetchAssignedStaff();
                  }
              } catch (error) {
                  console.error("Error removing staff:", error);
                  alert("Could not remove staff.");
              }
          },
  
          async handleDeleteTrek() {
  if (!confirm("Are you sure you want to delete this trek? This cannot beundone.")) return;
              try {
                  const token = localStorage.getItem("token");
                  const res = await axios.post(
  `http://127.0.0.1:5000/api/admin/scheduled_treks/${this.trekId}/delete_trek`,
                      {},
                      { headers: { Authorization: `Bearer ${token}` } }
                  );
                  if (res.status === 200) {
                      alert("Trek deleted successfully");
                      this.$emit("go-back");
                  }
              } catch (error) {
                  console.error("Error deleting trek:", error);
                  alert("Could not delete trek.");
              }
          },
  
          isAlreadyAssigned(staffId) {
              return this.assigned_staff.some(s => s.staff_id === staffId);
          }
      }
  };
  </script> -->




<template>

    <div class="container-fluid bg-light vh-100">

        <div class="row">

            <nav class = "navbar navbar-expand-lg bg-light border-bottom px-2">

                <div class="container-fluid">

                    <span class = "navbar-brand">
                        <h1 class="mt-2 fw-semibold display-4">
                            Manage Trek
                        </h1>
                        <p class="fw-semibold text-muted ms-1">
                            Edit trek details, assign or remove staff
                        </p>
                    </span>

                    <div class="d-flex align-items-end">
                        <button @click="goBack" class="btn btn-secondary btn-lg px-4">
                            
                            Go Back

                        </button>
                    </div>
                </div>
            </nav>
        </div>

        <div class="container py-4">

            <div class="card shadow-sm border-0 mb-4">

                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        Trek Details
                    </h4>

                    <p class="text-muted fw-semibold mb-0">
                        Update the scheduled trek information
                    </p>

                </div>
                <div class="card-body">
                    
                    <form @submit.prevent="handleSaveTrek">
 
                        <div class="row g-3">

                            <div class="col-md-6">

                                <label class="form-label fw-semibold">Trek Name</label>

                                <input v-model="form.trek_name" type="text" class="form-control" placeholder="Trek Name">

                            </div>


                            <div class="col-md-3">

                                <label class="form-label fw-semibold">
                                    Start Date
                                </label>

                                <input v-model = "form.start_date" type = "date" class="form-control">

                            </div>

                            <div class="col-md-3">

                                <label class="form-label fw-semibold">
                                    
                                    End Date
                                
                                </label>

                                <input v-model = "form.end_date" type="date" class="form-control">

                            </div>

                            <div class = "col-md-3">
                                <label class="form-label fw-semibold">
                                    
                                    Total Slots
                                
                                </label>
                                <input v-model.number = "form.total_slots" type = "number" class = "form-control" placeholder = "Total Slots" min = "1">

                           </div>

                            <div class="col-md-3">

                                <label class="form-label fw-semibold">

                                    Available Slots
                                    
                                </label>
                                <input :value="form.available_slots" type="number" class="form-control bg-light" readonly>

                            </div>


                            <div class="col-md-3">
                                <label class="form-label fw-semibold">
                                    
                                    Price
                                
                                </label>
                                <input v-model.number = "form.price" type = "number" class="form-control" placeholder = "Price" min="0">
                            
                            </div>

                            <div class="col-md-3">

                                <label class="form-label fw-semibold">
                                    
                                    Status
                                
                                </label>
                                <select v-model = "form.status" class = "form-select">

                                    <option value="Open"> 
                                        Open
                                    </option>
                                    <option value="Closed">
                                        Closed
                                    </option>
                                    <option value = "Cancelled">
                                        Cancelled
                                    </option>
                                    <option value = "Completed">
                                        Completed
                                    </option>
                                </select>
                            </div>

                        </div>
                        <div class="mt-4">

                            <button type = "submit" class="btn btn-success px-5 fw-semibold">
                                Save Changes
                            </button>

                        </div>
                    </form>
                </div>
            </div>


            <div class = "card shadow-sm border-0 mb-4">

                <div class = "card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0"> 
                        
                        Assigned Staff
                    
                    </h4>
                    <p class = "text-muted fw-semibold mb-0">
                        
                        Staff currently assigned to this trek
                    
                    </p>

                </div>
                <div class="card-body">

                    <div v-if="assigned_staff.length === 0" class="text-muted">

                        No staff assigned to this trek yet.

                    </div>

                    <table v-else class="table table-hover table-striped">
                        <thead>
                            <tr>
                                <th>
                                    Staff Name
                                </th>
                                <th>
                                    Email
                                </th>
                                <th>
                                    Phone
                                </th>
                                <th class="text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for = "staff in assigned_staff" :key="staff.assignment_id">
                                <td> 
                                    {{ staff.staff_name }}
                                </td>
                                <td>
                                    {{ staff.staff_email }}
                                </td>
                                <td>
                                    {{ staff.staff_phone }}
                                </td>
                                <td class="text-center">

                                    <button @click="handleRemoveStaff(staff.assignment_id)" class="btn btn-sm btn-outline-danger px-3">
                                        Remove
                                    </button>

                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>



            <div class="card shadow-sm border-0 mb-4">

                <div class="card-header bg-white border-bottom">

                    <h4 class="fw-semibold mb-0">
                        
                        Available Staff
                    
                    </h4>
                    <p class="text-muted fw-semibold mb-0">
                        
                        Select staff to assign to this trek
                    
                    </p>
                </div>
                <div class="card-body">

                    <div v-if="all_staff.length === 0" class="text-muted">

                        No staff available.

                    </div>
                    <table v-else class="table table-hover table-striped">
                        <thead>
                            <tr>
                                <th>
                                    Staff Name
                                </th>
                                <th>
                                    Email
                                </th>
                                <th>
                                    Phone
                                </th>
                                <th class="text-center">
                                    Action
                                </th>
                            </tr>
                        </thead>

                        <tbody>

                            <tr v-for="staff in all_staff" :key="staff.id">
                                <td>
                                    {{ staff.name }}
                                </td>
                                <td>
                                    {{ staff.email }}
                                </td>
                                <td>
                                    {{ staff.phone }}
                                </td>

                                <td class="text-center">

                                    <button  @click="handleAssignStaff(staff.id)"  class="btn btn-sm btn-outline-success px-3" :disabled="isAlreadyAssigned(staff.id)">

                                        {{ isAlreadyAssigned(staff.id) ? 'Assigned' : 'Add Staff' }}

                                    </button>

                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>



            <div class="card shadow-sm border-0 border-danger mb-5">

                <div class="card-header bg-white border-bottom border-danger">

                    <h4 class="fw-semibold text-danger mb-0">
                        Danger Zone
                    </h4>
                </div>
                <div class="card-body d-flex align-items-center justify-content-between">
                    <div>

                        <p class="fw-semibold mb-0"> 
                            Delete this trek
                        
                        </p>
                        <p class="text-muted small mb-0">
                            
                            This action is permanent and cannot be undone
                        
                        </p>
                    
                    </div>

                    <button @click="handleDeleteTrek" class="btn btn-danger px-5 fw-semibold">

                        Delete Trek

                    </button>

                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "ManageScheduledTrek",

    props: {
        trekId: {

            type: Number,
            required: true
        }
    },

    data() {
        return {
            // snapshot of what came from the API — used to compute the available slots diff
            originalTotalSlots: 0,
            originalAvailableSlots: 0,

            form: {
                trek_name: "",
                start_date: "",
                end_date: "",
                total_slots: 0,
                available_slots: 0,
                price: 0,
                status: "Open"
            },


            assigned_staff: [],
            all_staff: []
        };
    },

    watch: {                                         
        // whenever total_slots changes, recalculate available_slots
        // logic: available_slots = originalAvailableSlots + (new total - original total)
        // this preserves already-booked slots and only adjusts for the capacity change

        "form.total_slots"(newVal) {

            const diff = Number(newVal) - this.originalTotalSlots;

            const newAvailable = this.originalAvailableSlots + diff;

            this.form.available_slots = newAvailable;

        }
    },

    mounted() {
        this.fetchTrekDetails();
        this.fetchAssignedStaff();
        this.fetchAllStaff();
    },

    methods: {
        goBack() {
            this.$emit("go-back");
        },

        async fetchTrekDetails() {                                  // this is to fetch the trek details and show inside the from input fields as pre filled 
            try {

                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/admin/scheduled_trek/${this.trekId}`, {

                    headers: { 

                        Authorization: `Bearer ${token}` 
                    }

                });
                if (res.status === 200) {
                    
                    const t = res.data.trek;

                    this.form.trek_name      = t.trek_name;
                    this.form.start_date     = t.start_date;
                    this.form.end_date       = t.end_date;
                    this.form.total_slots    = Number(t.total_slots);
                    this.form.available_slots = Number(t.available_slots);
                    this.form.price          = t.price;
                    this.form.status         = t.status;

                    this.originalTotalSlots     = Number(t.total_slots);     //these two are used so that the admin can see the diff in the available slots
                    this.originalAvailableSlots = Number(t.available_slots);
                }
            } catch (error) {

                console.error("Error fetching trek details:", error);

            }
        },

        async fetchAssignedStaff() {

            try {

                const token = localStorage.getItem("token");

                const res = await axios.get(`http://127.0.0.1:5000/api/admin/treks/${this.trekId}/staff`, {
                    
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (res.status === 200) {

                    this.assigned_staff = res.data.assigned_staff;

                }
            } catch (error) {
                console.error("Error fetching assigned staff:", error);
            }
        },

        async fetchAllStaff() {                                // this is to fetch all the assigned staff 
            try {
                const token = localStorage.getItem("token");

                const res = await axios.get("http://127.0.0.1:5000/api/admin/all_staffs", {

                    headers: { Authorization: `Bearer ${token}` }

                });
                if (res.status === 200) {

                    this.all_staff = res.data.staffs;

                }
            } catch (error) {

                console.error("Error fetching all staff:", error);

            }
        },


        async handleSaveTrek() {


            try {

                const token = localStorage.getItem("token");

                const res = await axios.put(`http://127.0.0.1:5000/api/admin/scheduled_treks/${this.trekId}/update_trek`, this.form, { 
                    
                    headers: { 
                        
                        Authorization: `Bearer ${token}`
                    
                    } 
                
                });
                if (res.status === 200) {

                                                                                     // update originals so further edits in the same session are relative to the saved state
                    this.originalTotalSlots = Number(this.form.total_slots);
                    this.originalAvailableSlots = Number(this.form.available_slots);

                    alert("Trek updated successfully");

                }

            } catch (error) {

                if (error.response && error.response.status === 400) {

                    this.errors = error.response.data.errors || {};
                } else {

                    alert("Something went wrong while saving.");
                }
            }
        },

        async handleAssignStaff(staffId) {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.post(
                    `http://127.0.0.1:5000/api/admin/treks/${this.trekId}/assign_staff`,

                    { staff_id: staffId },
                    
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                if (res.status === 200) {
                    await this.fetchAssignedStaff();
                }
            } catch (error) {
                console.error("Error assigning staff:", error);
                alert("Could not assign staff.");
            }
        },

        async handleRemoveStaff(assignmentId) {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.post(
                    `http://127.0.0.1:5000/api/admin/assignments/${assignmentId}`,
                    { trek_id: this.trekId },
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                if (res.status === 200) {
                    await this.fetchAssignedStaff();
                }
            } catch (error) {
                console.error("Error removing staff:", error);
                alert("Could not remove staff.");
            }
        },

        async handleDeleteTrek() {
            if (!confirm("Are you sure you want to delete this trek? This cannot be undone.")) return;
            try {
                const token = localStorage.getItem("token");
                const res = await axios.post(
                    `http://127.0.0.1:5000/api/admin/scheduled_treks/${this.trekId}/delete_trek`,
                    {},
                    { headers: { Authorization: `Bearer ${token}` } }
                );
                if (res.status === 200) {
                    alert("Trek deleted successfully");
                    this.$emit("go-back");
                }
            } catch (error) {
                console.error("Error deleting trek:", error);
                alert("Could not delete trek.");
            }
        },

        isAlreadyAssigned(staffId) {
            return this.assigned_staff.some(s => s.staff_id === staffId);
        }
    }
};
</script>