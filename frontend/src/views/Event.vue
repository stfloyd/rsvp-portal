<template>
  <div v-if="isLoaded">
    <page-header
      :title="state.event.title"
      :subtitle="state.event.subtitle"
      :parentTitle="state.registration.title"
      :parentSubtitle="state.registration.subtitle"
      :showBackButton="true"
      @click-back="goBack()"
    />
    <div class="container">
      <section>
        <div class="text-left">
          <registration-form v-bind:event="state.event" />
        </div>
      </section>
    </div>
  </div>
</template>

<style></style>

<script lang="ts">
import { ref, defineComponent, onBeforeMount, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppService from '@/services/app'
import RegistrationForm from '@/components/RegistrationForm.vue'
import PageHeader from '@/components/PageHeader.vue'

export default defineComponent({
  components: {
    RegistrationForm,
    PageHeader
  },
  setup() {
    const router = useRouter()

    const state = ref({
      registration: null,
      event: null
    })

    const isLoaded = computed(() => {
      return state.value.registration != null && state.value.event != null
    })

    const goBack = async () => {
      const registrationSlug = router.currentRoute.value.params.registrationSlug as string
      router.push({ name: 'registration', params: { registrationSlug } })
    }

    const fetchRegistrationData = async (registrationSlug: string, eventSlug: string) => {
      const registration = await AppService.getRegistration(registrationSlug)
      state.value.registration = registration
      const event = await AppService.getEvent(registration, eventSlug)
      state.value.event = event
    }

    onBeforeMount(() => {
      const registrationSlug = router.currentRoute.value.params.registrationSlug as string
      const eventSlug = router.currentRoute.value.params.eventSlug as string

      fetchRegistrationData(registrationSlug, eventSlug).catch(e => {
        console.log(e)
        router.push({ name: 'home' })
      })
    })

    return { state, isLoaded, goBack }
  }
})
</script>
