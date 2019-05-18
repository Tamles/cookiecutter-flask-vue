<template>
  <div>
    <a-table
      :columns="columns"
      :dataSource="bangumis"
      :loading="loading"
      :pagination="pagination"
      @change="handleTableChange"
      bordered
    >
      <template
        v-for="col in ['name', 'time', 'url']"
        :slot="col"
        slot-scope="text, record"
      >
        <div :key="col">
          <a-input
            v-if="record.editable"
            style="margin: -5px 0"
            :value="text"
            @change="e => handleChange(e.target.value, record.key, col)"
          />
          <template v-else>
            <div v-if="col == 'time'">{{ moment(text).format("LL") }}</div>
            <div v-else-if="col == 'url'">
              <a target="_blank" :href="text"><a-icon type="link"></a-icon></a>
            </div>
            <div v-else>{{ text }}</div>
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <span v-if="record.editable">
          <a @click="() => save(record.key)"> <a-icon type="save"/></a>
          <a-popconfirm title="确定取消？" @confirm="() => cancel(record.key)">
            <a> <a-icon type="close"/></a>
          </a-popconfirm>
        </span>
        <span v-else>
          <a @click="() => edit(record.key)"> <a-icon type="edit"/></a>
        </span>
        <a-divider type="vertical" />
        <a-popconfirm
          v-if="bangumis.length"
          title="确定删除?"
          @confirm="() => onDelete(record.key)"
        >
          <a href="javascript:;"> <a-icon type="delete"/></a>
        </a-popconfirm>
      </template>
      <template slot="title">
        番剧列表
      </template>
      <template slot="footer">
        <a-button type="primary" @click="showModal">添加番剧</a-button>
        <bangumi-creation-form
          ref="bangumiForm"
          :visible="visible"
          @cancel="handleCancel"
          @create="handleCreate"
        />
      </template>
    </a-table>
  </div>
</template>

<script>
import BangumiCreationForm from "@/components/BangumiCreationForm";
import axios from "axios";
import moment from "moment";

const bangumiApi = "http://localhost:5000/api/v1/bangumis";

const columns = [
  {
    title: "番剧名",
    dataIndex: "name",
    scopedSlots: { customRender: "name" }
  },
  {
    title: "上映时间",
    dataIndex: "time",
    scopedSlots: { customRender: "time" }
  },
  {
    title: "链接",
    dataIndex: "url",
    scopedSlots: { customRender: "url" }
  },
  {
    title: "操作",
    dataIndex: "operation",
    scopedSlots: { customRender: "operation" }
  }
];

export default {
  name: "BangumiListTable",
  components: {
    BangumiCreationForm
  },
  mounted() {
    this.fetch();
  },
  data() {
    return {
      columns,
      bangumis: [],
      cacheData: [],
      visible: false,
      loading: false,
      pagination: {}
    };
  },
  methods: {
    fetch(params = {}) {
      this.loading = true;
      axios
        .get(bangumiApi, { params })
        .then(res => {
          this.bangumis = res.data.results.map(bangumi => ({
            ...bangumi,
            key: bangumi.id
          }));
          this.loading = false;
          const pagination = { ...this.pagination };
          pagination.total = res.data.total;
          pagination.pageSize = res.data.page_size;
          this.pagination = pagination;
        })
        .catch(err => {
          console.log(err);
        });
    },
    moment(date) {
      return moment(date);
    },
    showModal() {
      this.visible = true;
    },
    handleCancel() {
      this.visible = false;
    },
    handleCreate() {
      const form = this.$refs.bangumiForm.form;
      form.validateFields((err, values) => {
        if (err) {
          return;
        }
        axios.post(bangumiApi, values).then(res => {
          this.bangumis.push({ ...res.data, key: res.data.id });
        });
        form.resetFields();
        this.visible = false;
      });
    },
    handleTableChange(pagination) {
      const pager = { ...this.pagination };
      pager.current = pagination.current;
      this.pagination = pager;
      this.fetch({
        page: pagination.current
      });
    },
    onDelete(key) {
      const bangumis = [...this.bangumis];
      axios
        .delete(`${bangumiApi}/${key}`)
        .then(() => {
          this.bangumis = bangumis.filter(item => item.key !== key);
        })
        .catch(err => {
          console.log(err);
        });
    },
    handleChange(value, key, column) {
      const bangumis = [...this.bangumis];
      const target = bangumis.filter(item => key === item.key)[0];
      if (target) {
        target[column] = value;
        this.bangumis = bangumis;
      }
    },
    edit(key) {
      const bangumis = [...this.bangumis];
      const target = bangumis.filter(item => key === item.key)[0];
      if (target) {
        target.editable = true;
        this.bangumis = bangumis;
      }
    },
    save(key) {
      const bangumis = [...this.bangumis];
      const target = bangumis.filter(item => key === item.key)[0];
      if (target) {
        delete target.editable;
        console.log(target);
        axios
          .put(`${bangumiApi}/${key}`, target)
          .then(() => {
            this.bangumis = bangumis;
            this.cacheData = bangumis.map(item => ({ ...item }));
          })
          .catch(err => console.log(err));
      }
    },
    cancel(key) {
      const bangumis = [...this.bangumis];
      const target = bangumis.filter(item => key === item.key)[0];
      if (target) {
        Object.assign(
          target,
          this.cacheData.filter(item => key === item.key)[0]
        );
        delete target.editable;
        this.bangumis = bangumis;
      }
    }
  }
};
</script>
