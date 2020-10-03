export interface Registration {
  id: number
  title: string
  subtitle: string
  slug: string
  hide: boolean
}

export interface EventLocation {
  id: number
  name: string
  maxOccupancy: number
}

export interface RegistrationEvent {
  id: number
  registration: number
  title: string
  subtitle: string
  location: EventLocation
  maxOccupancy: number
  slug: string
  open: Date
  close: Date
  start: Date
  end: Date
  gradeOccupancies: []
  collectGuestNames: boolean
  childrenOnly: boolean
  excerpt: string
}

export interface Host {
  id: number
  firstName: string
  lastName: string
  email: string
  phoneNumber: string
}

export enum GuestVariant {
  Child,
  Adult
}

export interface GuestGrade {
  id: number
  name: string
  maxOccupancy: number
  currentOccupancy: number
}

export interface Guest {
  id: number
  host: number
  firstName: string
  lastName: string
  variant: GuestVariant
  grade: GuestGrade
}

export interface HostAttendance {
  host: Host
  event: RegistrationEvent
}

export interface GuestAttendance {
  guest: Guest
  event: RegistrationEvent
}

export interface Submission {
  event: Event
  host: Host
  guests: Guest[]
}
