import ApiService from './api'
import { Registration, RegistrationEvent, Guest, Host } from '@/interfaces/app'

class InvalidRegistration extends Error {
  errorCode: number

  constructor(errorCode: number, message: string) {
    super(message)
    this.name = this.constructor.name
    this.message = message
    this.errorCode = errorCode
  }
}

class InvalidHostRegistration extends InvalidRegistration {}

class InvalidGuestRegistration extends InvalidRegistration {}

const AppService = {
  getRegistrations: async function() {
    const response = await ApiService.get('/registrations/')
    return response.data.results as Registration[]
  },

  getRegistration: async function(slug: string) {
    const registrations = await this.getRegistrations()

    const matches = registrations.filter(item => {
      return item.slug === slug
    })

    console.log(`Potential matches for slug '${slug}': ${JSON.stringify(matches)}`)

    if (matches.length > 0) {
      return matches[0]
    } else {
      throw new InvalidRegistration(404, `Registration with slug '${slug}' does not exist`)
    }
  },

  getEvents: async function(registration: Registration) {
    const response = await ApiService.get(`/events/`)
    const events = response.data.results.filter(
      (element: RegistrationEvent) => element.registration == registration.id
    )
    return events as RegistrationEvent[]
  },

  getEvent: async function(registration: Registration, slug: string) {
    let events: RegistrationEvent[]

    try {
      events = await this.getEvents(registration)
    } catch (e) {
      throw new InvalidRegistration(e.response.status, 'Invalid event')
    }

    const matches = events.filter(item => {
      return item.slug === slug
    })

    console.log(`Potential matches for slug '${slug}': ${JSON.stringify(matches)}`)

    if (matches.length > 0) {
      return matches[0] as RegistrationEvent
    } else {
      throw new InvalidRegistration(404, `Event with slug '${slug}' does not exist`)
    }
  },

  postHost: async function(host: Host, event: RegistrationEvent) {
    try {
      const response = await ApiService.post('/hosts/', host)
      return response
    } catch (e) {
      console.log(event)
      throw new InvalidHostRegistration(e.response.status, 'Invalid host')
    }
  },

  postGuests: async function(guests: Guest[], event: RegistrationEvent) {
    let guestsResponse: Guest[]

    try {
      const response = await ApiService.post('/guests/', guests)
      guestsResponse = response.data
      console.log(response.data)
    } catch (e) {
      console.log(e.response)
      throw new InvalidGuestRegistration(e.response.status, 'Invalid guest(s)')
    }

    if (event) {
      const guestRSVPs: { guest: number; event: number }[] = []
      guestsResponse.forEach((guest: Guest) => {
        guestRSVPs.push({
          guest: guest.id,
          event: event.id
        })
      })

      console.log(guestRSVPs)

      await ApiService.post('/guest-rsvp/', guestRSVPs)
    }

    return guestsResponse
  },

  sendConfirmation: async function(host: Host, event: RegistrationEvent) {
    try {
      await ApiService.post('/mail-confirmation/', { host: host.id, event: event.id })
    } catch (e) {
      console.log(e)
      //throw new InvalidRegistration(e.response.status, 'Unable to send e-mail confirmation')
    }
  }
}

export default AppService
