<template>
  <div>
    <a-modal
      title="添加番剧"
      :visible="visible"
      ok-text="保存"
      cancel-text="取消"
      @cancel="
        () => {
          $emit('cancel');
        }
      "
      @ok="
        () => {
          $emit('create');
        }
      "
    >
      <a-form :form="form">
        <a-form-item>
          <a-input
            v-decorator="[
              'name',
              { rules: [{ required: true, message: '请输入番剧名！' }] }
            ]"
            placeholder="番剧名"
          />
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'time',
              { rules: [{ required: true, message: '请输入上映时间！' }] }
            ]"
            placeholder="上映时间（格式：YYYY-MM-DD）"
          />
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'url',
              { rules: [{ required: true, message: '请输入链接！' }] }
            ]"
            placeholder="链接"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
export default {
  name: 'BangumiCreationForm',
  props: {
    visible: Boolean
  },
  beforeCreate() {
    this.form = this.$form.createForm(this)
  }
}
</script>
