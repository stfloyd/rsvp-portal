<template>
  <form style="margin-right:auto;margin-left:auto;max-width:75%;">
    <div
      v-if="error"
      :class="
        'toast mt-3 mr-3 text-light ' + (error.title == 'Success' ? 'bg-success' : 'bg-danger')
      "
      style="position:fixed;opacity:100;top:0;right:0;"
    >
      <div
        :class="
          'toast-header text-light ' + (error.title == 'Success' ? 'bg-success' : 'bg-danger')
        "
      >
        {{ error.title }}
      </div>
      <div class="toast-body">{{ error.message }}</div>
    </div>
    <div class="form-row">
      <div class="form-group col-md-6">
        <label for="firstName">Parent First Name</label>
        <input
          type="text"
          class="form-control"
          id="firstName"
          placeholder="First Name"
          v-model="state.host.firstName"
        />
      </div>
      <div class="form-group col-md-6">
        <label for="lastName">Parent Last Name</label>
        <input
          type="text"
          class="form-control"
          id="lastName"
          placeholder="Last Name"
          v-model="state.host.lastName"
        />
      </div>
    </div>
    <div class="form-group">
      <label for="emailAddress">Parent E-Mail Address</label>
      <input
        type="email"
        class="form-control"
        id="emailAddress"
        placeholder="user@domain.com"
        v-model="state.host.email"
      />
    </div>
    <div v-if="collectPhone" class="form-group">
      <label for="phoneNumber">Phone #</label>
      <input
        type="text"
        class="form-control"
        id="phoneNumber"
        placeholder="(000) 000-0000"
        v-model="state.host.phone"
      />
    </div>
    <div v-if="collectGuests">
      <h2 class="container mt-4">
        <span v-if="event.childrenOnly">Children</span>
        <span v-else>Guests</span>
        <button
          type="button"
          v-on:click="addGuest()"
          class="btn btn-success float-right"
          v-if="initialGuestCount + state.guests.length < maximumGuestCount"
        >
          <span v-if="event.childrenOnly">Add Child</span>
          <span v-else>Add Guest</span>
        </button>
      </h2>
      <hr class="mb-3" />
      <div v-for="(guest, index) in state.guests" :key="`guest-${index}`">
        <h4>
          <span v-if="event.childrenOnly">Child #{{ index + 1 }}</span>
          <span v-else>Guest #{{ index + 1 }}</span>
          <div v-if="state.guests.length > 1" class="btn-toolbar float-right">
            <div class="btn-group">
              <button type="button" class="btn btn-danger" v-on:click="deleteGuest(index)">
                <span class="fa fa-trash"></span>
              </button>
            </div>
          </div>
        </h4>
        <div v-if="event.collectGuestNames" class="form-row">
          <div class="form-group col-md-6">
            <label for="firstName">First Name</label>
            <input
              type="text"
              class="form-control"
              id="firstName"
              placeholder="First Name"
              v-model="state.guests[index].firstName"
            />
          </div>
          <div class="form-group col-md-6">
            <label for="lastName">Last Name</label>
            <input
              type="text"
              class="form-control"
              id="lastName"
              placeholder="Last Name"
              v-model="state.guests[index].lastName"
            />
          </div>
        </div>
        <div class="form-row">
          <div :class="!event.childrenOnly ? 'form-group col-md-6' : 'form-group col-12'">
            <label :for="`guest-${index}-grade`">Grade / Age Group</label>
            <select
              @change="onChangeGuestGrade($event, index)"
              class="custom-select"
              :id="`guest-${index}-grade`"
            >
              <option selected :value="-1">Choose...</option>
              <option
                v-for="(grade, gradeIndex) in state.gradeLevels"
                :value="grade.id"
                :data-index="gradeIndex"
                :key="`guest-${index}-grade-${gradeIndex}`"
                :disabled="grade.currentOccupancy >= grade.maxOccupancy"
                >{{ grade.name }} ({{ grade.currentOccupancy }} / {{ grade.maxOccupancy }})</option
              >
            </select>
          </div>
          <div class="form-group col-md-6" v-if="!event.childrenOnly">
            <label :for="`guest-${index}-variant`">Adult / Child</label>
            <select
              class="custom-select"
              :id="`guest-${index}-variant`"
              v-model="state.guests[index].variant"
            >
              <option selected :value="-1">Choose...</option>
              <option
                v-for="(variant, variantIndex) in state.guestVariants"
                :value="variant.value"
                :key="`guest-${index}-variant-${variantIndex}`"
                >{{ variant.text }}</option
              >
            </select>
          </div>
        </div>
        <hr />
      </div>
    </div>
    <div class="text-center my-5">
      <button
        type="button"
        class="btn btn-primary"
        :disabled="submitDisabled"
        v-on:click="submitRSVP()"
      >
        Submit
      </button>
    </div>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import {
  Guest,
  GuestVariant,
  GuestGrade,
  RegistrationEvent,
  Host,
  Submission
} from '@/interfaces/app'
import AppService from '../services/app'

function sleep(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export default defineComponent({
  props: {
    event: {
      type: Object,
      required: true
    },
    collectGuests: {
      type: Boolean,
      default: true
    },
    collectPhone: {
      type: Boolean,
      default: false
    },
    collectGuestVariant: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const router = useRouter()

    const state = ref({
      host: {
        id: null,
        firstName: '',
        lastName: '',
        phoneNumber: props.collectPhone ? '' : null,
        email: ''
      },
      guests: [
        {
          id: null,
          host: null,
          firstName: null,
          lastName: null,
          variant: GuestVariant.Child,
          grade: null
        }
      ],
      guestVariants: [
        { value: 0, text: 'Child' },
        { value: 1, text: 'Adult' }
      ],
      gradeLevels: props.event.gradeOccupancies,
      submitting: false
    })

    const error = ref(null)

    const initialGuestCount = state.value.gradeLevels.reduce((a: number, b: GuestGrade) => {
      return a + (b.currentOccupancy || 0)
    }, 0)

    const maximumGuestCount = computed(() =>
      state.value.gradeLevels.reduce((a: number, b: GuestGrade) => {
        return a + (b.maxOccupancy || 0)
      }, 0)
    )

    const addGuest = () => {
      state.value.guests.push({
        id: null,
        host: null,
        firstName: null,
        lastName: null,
        variant: GuestVariant.Child,
        grade: null
      })
    }

    const deleteGuest = (guestIndex: number) => {
      const gradeId = state.value.guests[guestIndex].grade
      state.value.guests.splice(guestIndex, 1)
      state.value.gradeLevels.forEach((element: GuestGrade, index: number) => {
        if (index == gradeId) {
          state.value.gradeLevels[index].currentOccupancy -= 1
        }
      })
    }

    // eslint-disable-next-line
    const onChangeGuestGrade = (event: any, guestIndex: number) => {
      let previousGradeId: number
      const gradeId = event.target.value as number
      const gradeIndex = event.target.options[event.target.options.selectedIndex].dataset.index

      if (state.value.guests[guestIndex].grade != null) {
        previousGradeId = state.value.guests[guestIndex].grade as number
      } else {
        previousGradeId = -1
      }

      if (previousGradeId >= 0) {
        state.value.gradeLevels.forEach((element: GuestGrade, index: number) => {
          if (index == previousGradeId) {
            state.value.gradeLevels[index].currentOccupancy -= 1
          }
        })
      }

      if (gradeIndex >= 0) {
        state.value.gradeLevels[gradeIndex].currentOccupancy += 1
        state.value.guests[guestIndex].grade = gradeId
      } else {
        state.value.guests[guestIndex].grade = null
      }
    }

    const submitDisabled = computed(() => {
      if (error.value) {
        if (error.value.title == 'Success') {
          return true
        }
      }

      let invalidData = true

      if (state.value.host.firstName && state.value.host.lastName && state.value.host.email) {
        invalidData = false

        if (props.collectGuests) {
          state.value.guests.forEach((guest: Guest) => {
            if (guest.grade == null) {
              invalidData = true
            }

            if (props.collectGuestVariant) {
              if (guest.variant == -1 || guest.variant == null) {
                invalidData = true
              }
            }

            if (props.event.collectGuestNames) {
              if (!guest.firstName || !guest.lastName) {
                invalidData = true
              }
            }
          })
        }
      }

      return invalidData
    })

    // TODO: Put this is a de-coupled module/component
    const showError = async (message: string) => {
      error.value = {
        title: 'Error',
        message: message
      }
      await sleep(2000)
      error.value = null
    }

    // TODO: Put this is a de-coupled module/component
    const showSuccess = async (message: string) => {
      error.value = {
        title: 'Success',
        message: message
      }
      await sleep(1000)
      error.value = null
    }

    const submitRSVP = async () => {
      state.value.submitting = true

      let hasError = false
      let host: Host
      const event: RegistrationEvent = props.event as RegistrationEvent

      try {
        const hostResponse = await AppService.postHost(state.value.host, null)
        host = hostResponse.data as Host

        state.value.guests.forEach((guest: Guest, index: number) => {
          state.value.guests[index].host = host.id

          if (!props.collectGuestVariant) {
            state.value.guests[index].variant = GuestVariant.Child
          }
        })

        await AppService.postGuests(state.value.guests, event)
      } catch (e) {
        hasError = true
        console.log(e)
        await showError('Had an issue locking in this RSVP, please refresh.')
      } finally {
        state.value.submitting = false
      }

      if (!hasError) {
        await AppService.sendConfirmation(host, event)
        router.push({
          name: 'confirmation',
          params: {
            eventTitle: props.event.title,
            eventSubtitle: props.event.subtitle,
            guestCount: state.value.guests.length,
            hostName: `${state.value.host.firstName} ${state.value.host.lastName}`
          }
        })
      } else {
        showError('Had an issue registering...').then(async () => {
          //window.location.href = ''
        })
      }
    }

    return {
      state,
      addGuest,
      deleteGuest,
      onChangeGuestGrade,
      submitDisabled,
      initialGuestCount,
      maximumGuestCount,
      submitRSVP,
      error
    }
  }
})
</script>

<style scoped>
label {
  font-weight: 550;
}
</style>
