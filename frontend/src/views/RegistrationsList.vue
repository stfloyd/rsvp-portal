<template>
  <div v-if="isLoaded">
    <page-header
      title="Registrations"
      subtitle="Please RSVP for child care for Sunday Service"
      :showBackButton="false"
    />
    <div class="container">
      <div
        v-if="visibleRegistrations.length > 0"
        class="card-deck"
        style="margin-right:auto;margin-left:auto;"
      >
        <div
          class="card"
          v-for="(registration, index) in visibleRegistrations"
          :key="`registration-${index}`"
        >
          <div class="card-header bg-primary text-light py-5" style="min-height:200;">
            <h4 class="card-title">{{ registration.title }}</h4>
            <p class="card-text" v-html="registration.subtitle" />
          </div>
          <div class="card-body">
            <router-link
              :to="{ name: 'registration', params: { registrationSlug: registration.slug } }"
              class="btn btn-primary stretched-link"
              >View Events</router-link
            >
          </div>
        </div>
      </div>
      <div v-else>
        <h2>There are currently no RSVP opportunities available, check back later.</h2>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onBeforeMount, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppService from '@/services/app'
import PageHeader from '@/components/PageHeader.vue'
import { Registration } from '../interfaces/app'

export default defineComponent({
  components: {
    PageHeader
  },
  setup() {
    const router = useRouter()

    const state = ref({
      registrations: null
    })

    const isLoaded = computed(() => {
      return state.value.registrations != null
    })

    const visibleRegistrations = computed(() => {
      return state.value.registrations.filter((registration: Registration) => !registration.hide)
    })

    const fetchRegistrationData = async () => {
      const registrations = await AppService.getRegistrations()
      state.value.registrations = registrations
    }

    onBeforeMount(() => {
      fetchRegistrationData().catch(e => {
        console.log(e)
        router.push({ name: 'home' })
      })
    })

    return { state, visibleRegistrations, isLoaded }
  }
})
</script>
