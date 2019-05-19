<template>
  <a-locale-provider :locale="zh_CN">
    <div id="app">
      <router-view />
    </div>
  </a-locale-provider>
</template>

<script>
import zh_CN from 'ant-design-vue/lib/locale-provider/zh_CN'

export default {
  name: 'App',
  data() {
    return {
      zh_CN
    }
  }
}
</script>
