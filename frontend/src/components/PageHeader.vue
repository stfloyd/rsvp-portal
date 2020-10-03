<template>
  <div class="container-fluid px-0 bg-white">
    <div class="container-fluid page-header py-4 pt-5">
      <div v-if="showBackButton" class="btn-toolbar float-left" style="position:absolute;">
        <div class="btn-group">
          <button v-on:click="onClickBack()" class="btn btn-danger btn-circle btn-xl">
            <span class="fa fa-chevron-left"></span>
          </button>
        </div>
      </div>
      <img src="" height="96" />
      <hr />
      <div class="pt-4">
        <h1 v-if="parentTitle" style="font-weight:300;">{{ parentTitle }}</h1>
        <h4 v-if="false" style="font-weight:300;">{{ parentSubtitle }}</h4>
        <h2 :style="parentTitle ? 'font-weight:400;' : 'font-weight:300;'">{{ title }}</h2>
        <h5 style="font-weight:400;" v-html="subtitle" />
      </div>
    </div>
    <hr />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  props: {
    showBackButton: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: null
    },
    parentTitle: {
      type: String,
      required: false
    },
    parentSubtitle: {
      type: String,
      required: false
    }
  },
  setup(props, context) {
    const onClickBack = () => {
      context.emit('click-back')
    }

    return {
      onClickBack
    }
  }
})
</script>

<style>
.btn-circle.btn-xl {
  width: 48px;
  height: 48px;
  border-radius: 35px;
  font-size: 18px;
}

.btn-circle {
  width: 30px;
  height: 30px;
  padding: 6px 0px;
  border-radius: 15px;
  text-align: center;
  font-size: 12px;
  line-height: 1.42857;
}
</style>
