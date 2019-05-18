<template>
  <div>
    <a-modal
      title="添加番剧"
      :visible="visible"
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
      okText="保存"
      cancelText="取消"
    >
      <a-form :form="form">
        <a-form-item>
          <a-input
            v-decorator="[
              'name',
              { rules: [{ required: true, message: '请输入番剧名！' }] }
            ]"
            placeholder="番剧名"
          >
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'time',
              { rules: [{ required: true, message: '请输入上映时间！' }] }
            ]"
            placeholder="上映时间（格式：YYYY-MM-DD）"
          >
          </a-input>
        </a-form-item>
        <a-form-item>
          <a-input
            v-decorator="[
              'url',
              { rules: [{ required: true, message: '请输入链接！' }] }
            ]"
            placeholder="链接"
          >
          </a-input>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
export default {
  name: "BangumiCreationForm",
  props: ["visible"],
  beforeCreate() {
    this.form = this.$form.createForm(this);
  }
};
</script>
