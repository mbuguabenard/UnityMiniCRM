<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { crmService } from '../services/api'

const router = useRouter()
const profile = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  job_title: '',
  company: null,
  bio: ''
})
const companies = ref([])
const companies_map = ref({})
const loading = ref(true)
const snackbar = ref(false)
const snackbarMessage = ref('')
const editMode = ref(false)
const hasLoadedProfile = ref(false)

// Check if profile is new/empty - only after data has loaded
const isNewProfile = computed(() => {
  if (!hasLoadedProfile.value) return false
  return !profile.value.first_name && !profile.value.last_name && !profile.value.email && !profile.value.phone
})

onMounted(async () => {
  try {
    loading.value = true
    const data = await crmService.getProfile()
    if (data) {
      profile.value = {
        id: data.id || null,
        username: data.username || '',
        first_name: data.first_name || '',
        last_name: data.last_name || '',
        email: data.email || '',
        phone: data.phone || '',
        job_title: data.job_title || '',
        department: data.department || '',
        company: data.company || null,
        bio: data.bio || '',
        profile_picture: data.profile_picture || null
      }
      hasLoadedProfile.value = true
    }
    const companiesList = await crmService.getCompanies()
    companies.value = companiesList
    companiesList.forEach(c => {
      companies_map.value[c.id] = c.name
    })
  } catch (err) {
    console.error('Failed to load profile:', err)
    hasLoadedProfile.value = true
  } finally {
    loading.value = false
  }
})

const save = async () => {
  try {
    await crmService.updateProfile(profile.value)
    snackbarMessage.value = 'Profile saved successfully!'
    snackbar.value = true
    editMode.value = false
    setTimeout(() => {
      if (isNewProfile.value) {
        router.push('/')
      }
    }, 1500)
  } catch (err) {
    console.error(err)
    snackbarMessage.value = 'Error saving profile'
    snackbar.value = true
  }
}

const toggleEdit = () => {
  editMode.value = !editMode.value
}
</script>

<template>
  <v-container class="pa-6">
    <!-- New Profile Form -->
    <v-card v-if="!loading && isNewProfile" elevation="4">
      <v-card-title class="text-h5 font-weight-bold bg-gradient pa-6">
        <v-icon class="mr-3">mdi-account-plus</v-icon>
        Complete Your Profile
      </v-card-title>
      
      <v-card-text class="pa-6">
        <v-alert type="info" class="mb-6" icon="mdi-information">
          Welcome! Complete your profile to get started and customize your experience.
        </v-alert>
        
        <v-form>
          <v-text-field 
            v-model="profile.first_name" 
            label="First name *" 
            required 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.last_name" 
            label="Last name *" 
            required 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.email" 
            label="Email *" 
            type="email" 
            required 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.phone" 
            label="Phone" 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.job_title" 
            label="Job title" 
            variant="outlined"
            class="mb-4"
          />
          <v-select 
            v-model="profile.company" 
            :items="companies" 
            item-title="name" 
            item-value="id" 
            label="Company" 
            clearable 
            variant="outlined"
            class="mb-4"
          />
          <v-textarea 
            v-model="profile.bio" 
            label="About you" 
            rows="4" 
            variant="outlined"
          />
        </v-form>
      </v-card-text>
      
      <v-card-actions class="pa-6">
        <v-spacer></v-spacer>
        <v-btn color="primary" size="large" @click="save">
          <v-icon class="mr-2">mdi-check</v-icon>
          Register Now
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Saved Profile - Read-Only Display -->
    <v-card v-else-if="!loading && !isNewProfile && !editMode" elevation="3">
      <v-card-title class="text-h5 font-weight-bold pa-6">
        <v-icon class="mr-3">mdi-account-circle</v-icon>
        {{ profile.first_name }} {{ profile.last_name }}
      </v-card-title>
      
      <v-divider></v-divider>
      
      <v-card-text class="pa-6">
        <v-row>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">First Name</label>
              <div class="text-body-1 mt-2">{{ profile.first_name }}</div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">Last Name</label>
              <div class="text-body-1 mt-2">{{ profile.last_name }}</div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">Email</label>
              <div class="text-body-1 mt-2">{{ profile.email }}</div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">Phone</label>
              <div class="text-body-1 mt-2">{{ profile.phone || 'Not provided' }}</div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">Job Title</label>
              <div class="text-body-1 mt-2">{{ profile.job_title || 'Not provided' }}</div>
            </div>
          </v-col>
          <v-col cols="12" md="6">
            <div class="mb-6">
              <label class="text-overline text-grey-darken-1 font-weight-bold">Company</label>
              <div class="text-body-1 mt-2">
                <v-chip v-if="profile.company" variant="tonal" prepend-icon="mdi-office-building">
                  {{ companies_map[profile.company] || 'Unknown' }}
                </v-chip>
                <span v-else class="text-grey">Not assigned</span>
              </div>
            </div>
          </v-col>
          <v-col cols="12">
            <div>
              <label class="text-overline text-grey-darken-1 font-weight-bold">About You</label>
              <div class="text-body-2 mt-2">{{ profile.bio || 'No bio provided' }}</div>
            </div>
          </v-col>
        </v-row>
      </v-card-text>
      
      <v-divider></v-divider>
      
      <v-card-actions class="pa-6">
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="tonal" @click="toggleEdit">
          <v-icon class="mr-2">mdi-pencil</v-icon>
          Edit Profile
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Edit Mode Form -->
    <v-card v-else-if="!loading && !isNewProfile && editMode" elevation="4">
      <v-card-title class="text-h5 font-weight-bold pa-6">
        <v-icon class="mr-3">mdi-pencil-circle</v-icon>
        Edit Profile
      </v-card-title>
      
      <v-divider></v-divider>
      
      <v-card-text class="pa-6">
        <v-form>
          <v-text-field 
            v-model="profile.first_name" 
            label="First name" 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.last_name" 
            label="Last name" 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.email" 
            label="Email" 
            type="email" 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.phone" 
            label="Phone" 
            variant="outlined"
            class="mb-4"
          />
          <v-text-field 
            v-model="profile.job_title" 
            label="Job title" 
            variant="outlined"
            class="mb-4"
          />
          <v-select 
            v-model="profile.company" 
            :items="companies" 
            item-title="name" 
            item-value="id" 
            label="Company" 
            clearable 
            variant="outlined"
            class="mb-4"
          />
          <v-textarea 
            v-model="profile.bio" 
            label="About you" 
            rows="4" 
            variant="outlined"
          />
        </v-form>
      </v-card-text>
      
      <v-divider></v-divider>
      
      <v-card-actions class="pa-6">
        <v-btn color="grey" variant="text" @click="toggleEdit">
          <v-icon class="mr-2">mdi-close</v-icon>
          Cancel
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="save">
          <v-icon class="mr-2">mdi-check</v-icon>
          Save Changes
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Loading State -->
    <div v-if="loading" class="text-center pa-12">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </div>

    <!-- Success/Error Snackbar -->
    <v-snackbar
      v-model="snackbar"
      :timeout="2000"
      location="bottom"
      color="success"
    >
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>