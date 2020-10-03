<template>
  <div v-if="isLoaded">
    <page-header
      :title="state.registration.title"
      :subtitle="state.registration.subtitle"
      :showBackButton="false"
      @click-back="goBack()"
    />
    <div class="container">
      <div
        v-if="visibleEvents.length > 0"
        class="card-deck"
        style="margin-right:auto;margin-left:auto;max-width:75%;"
      >
        <div class="card" v-for="(event, index) in visibleEvents" :key="`event-${index}`">
          <div class="card-header bg-primary text-light pt-5 pb-4" style="min-height:200;">
            <h4 class="card-title">{{ event.title }}</h4>
          </div>
          <div class="card-body">
            <strong class="card-text">{{ getEventDateString(event.start) }}</strong>
            <div class="card-text">
              <div>{{ getEventTimeString(event.start) }} - {{ getEventTimeString(event.end) }}</div>
              <div v-if="event.excerpt">
                {{ event.excerpt }}
              </div>
            </div>
            <router-link
              v-if="!isEventFilled(event)"
              :to="{
                name: 'registration-event',
                params: { registrationSlug: state.registration.slug, eventSlug: event.slug }
              }"
              class="btn btn-lg mt-3 btn-primary stretched-link"
              >Register</router-link
            >
            <strong v-else>Maximum capacity reached</strong>
          </div>
        </div>
      </div>
      <div v-else>
        <h2 class="mt-5 pt-5">Unfortunately, there are no events currently open for RSVP.</h2>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, defineComponent, onBeforeMount, computed } from 'vue'
import { useRouter } from 'vue-router'
import AppService from '@/services/app'
import { RegistrationEvent, GuestGrade } from '@/interfaces/app'
import PageHeader from '@/components/PageHeader.vue'

export default defineComponent({
  components: {
    PageHeader
  },
  setup() {
    const router = useRouter()

    const showBackButton = false

    const state = ref({
      registration: null,
      events: null
    })

    const isLoaded = computed(() => {
      return state.value.registration != null && state.value.events != null
    })

    const visibleEvents = computed(() => {
      if (isLoaded.value) {
        const now = new Date()
        return state.value.events.filter((e: RegistrationEvent) => {
          const openDate = new Date(e.open)
          const closeDate = new Date(e.close)
          return now > openDate && now < closeDate
        })
      } else {
        return false
      }
    })

    const goBack = async () => {
      router.push({ name: 'registrations' })
    }

    const fetchRegistrationData = async (slug: string) => {
      const registration = await AppService.getRegistration(slug)
      state.value.registration = registration
      const events = await AppService.getEvents(registration)
      state.value.events = events
    }

    const getEventDateString = (date: Date) => {
      const ishygddt = new Date(date)
      const year = ishygddt.getFullYear()
      const month = ishygddt.toLocaleDateString('default', { month: 'short' })
      const day = ishygddt.getDate()
      return `${month} ${day}, ${year}`
    }

    const getEventTimeString = (date: Date) => {
      const dateObj = new Date(date)
      let hours = dateObj.getHours()
      const minutes = dateObj.getMinutes()
      const ampm = hours >= 12 ? 'PM' : 'AM'
      hours = hours % 12
      hours = hours ? hours : 12 // the hour '0' should be '12'

      let minuteStr: string
      if (minutes < 10) {
        minuteStr = '0' + minutes
      } else {
        minuteStr = '' + minutes
      }

      const strTime = hours + ':' + minuteStr + ' ' + ampm
      return strTime
    }

    const isEventFilled = (event: RegistrationEvent) => {
      let allGradesReserved = true

      event.gradeOccupancies.forEach((grade: GuestGrade) => {
        if (grade.currentOccupancy < grade.maxOccupancy) {
          allGradesReserved = false
        }
      })

      return allGradesReserved
    }

    onBeforeMount(() => {
      fetchRegistrationData(router.currentRoute.value.params.registrationSlug as string).catch(
        e => {
          console.log(e)
          router.push({ name: 'home' })
        }
      )
    })

    return {
      state,
      visibleEvents,
      isLoaded,
      showBackButton,
      goBack,
      isEventFilled,
      getEventDateString,
      getEventTimeString
    }
  }
})
</script>
