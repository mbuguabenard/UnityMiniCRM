<template>
  <v-container class="pa-4" max-width="600">
    <v-card>
      <v-card-title>Register</v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field v-model="email" label="Email" required />
          <v-text-field v-model="first_name" label="First name" />
          <v-text-field v-model="last_name" label="Last name" />
          <v-text-field v-model="password" label="Password" type="password" required />
        </v-form>
        <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="register" :loading="loading">Register</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authService } from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const first_name = ref('')
const last_name = ref('')
const loading = ref(false)
const error = ref(null)
const valid = ref(false)

async function register() {
  error.value = null
  if (!email.value || !password.value) {
    error.value = 'Email and password required'
    return
  }
  loading.value = true
  try {
    const data = await authService.signup(email.value, password.value, first_name.value, last_name.value)
    if (data.token) {
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      router.push('/profile')
    } else if (data.error) {
      error.value = data.error
    }
  } catch (e) {
    error.value = e?.response?.data?.error || e.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
