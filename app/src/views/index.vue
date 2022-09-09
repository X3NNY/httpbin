<template>
  <div class="box">
    <div class="header">
      <a href="https://github.com/X3NNY/httpbin" style="text-decoration: none;color: unset !important;"><p>HTTPBin</p></a>
      <div>
        <el-switch
          v-model="dark"
          style="margin-left: 24px"
          inline-prompt
          :active-icon="Moon"
          :inactive-icon="Sunny"
          @change="switchTheme"
        />
        <a href="https://github.com/X3NNY/httpbin" target="_blank"><el-button text><el-icon><Paperclip /></el-icon></el-button></a>
        <a href="https://www.ctfer.vip/" target="_blank"><el-button text><el-icon><MagicStick /></el-icon></el-button></a>
        <a href="https://github.com/element-plus/element-plus" target="_blank"><el-button text><el-icon><ElementPlus /></el-icon></el-button></a>
      </div>

    </div>
    <el-scrollbar style="height:92vh">
      <router-view></router-view>
    </el-scrollbar>
  </div>
</template>

<script>
import themes from '@/utils/themes'
import {colorMix} from "@/utils/tool"
import { Moon, Sunny } from '@element-plus/icons-vue'

export default {
  name: "Theme",
  components: {
  },
  data() {
    return {
      Moon,
      Sunny,
      dark: true,
      themeObj: {}
    };
  },
  mounted() {
    this.switchTheme(true)
  },
  methods: {
    switchTheme(type) {
      this.dark = type || false
      this.themeObj = themes[this.dark?'darkTheme':'lightTheme']

      this.getsTheColorScale()

      Object.keys(this.themeObj).map(item => {
        document.documentElement.style.setProperty(item, this.themeObj[item])
      })
    },

    getsTheColorScale() {
      const colorList = ['primary', 'success', 'warning', 'danger', 'error', 'info']
      const prefix = '--el-color-'
      colorList.map(colorItem => {
        for (let i = 1; i < 10; i += 1) {
          if (i === 2) {
            this.themeObj[`${prefix}${colorItem}-dark-${2}`] = colorMix(this.themeObj[`${prefix}black`], this.themeObj[`${prefix}${colorItem}`], 1)
          } else {
            this.themeObj[`${prefix}${colorItem}-light-${10 - i}`] = colorMix(this.themeObj[`${prefix}white`], this.themeObj[`${prefix}${colorItem}`], i * 0.1)
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.box {
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
  background: var(--el-bg-color);

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 2vw;
    height: 6vh;
    font-size: 30px;
    font-weight: bold;
    color: var(--el-text-color-primary);
    background: var(--el-bg-color);
    border-bottom: 4px solid var(--el-color-black);
  }
}
</style>