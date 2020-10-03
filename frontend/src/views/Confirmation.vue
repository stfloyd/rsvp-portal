<template>
  <div>
    <page-header :title="eventTitle" subtitle="You successfully registered your children!" />
    <div class="container">
      <p>You registered {{ guestCount }} guest(s).</p>
      <p>Please check your e-mail for confirmation! Check junk-mail / spam folder if you do not see it.</p>
      <p>
        We look forward to seeing you! Please leave enough time to check your children in at the right locations so you can make it to the service on time!
        Please know that while preregistration tells our kids team to expect your child, capacity is limited due to Covid restrictions and final check-in at arrival will confirm availability.
      </p>
      <!--<a class="btn btn-primary" href="">Go Back To Kids</a>-->
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, computed } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/PageHeader.vue'

export default defineComponent({
  components: {
    PageHeader
  },
  props: {
    eventTitle: String,
    eventSubtitle: String,
    hostName: String,
    guestCount: Number
  },
  setup(props, context) {
    const router = useRouter()

    onBeforeMount(() => {
      if (!props.eventTitle || !props.eventSubtitle || !props.hostName) {
        router.push({ name: 'home' })
      }
    })

    return {}
  }
})
</script>
