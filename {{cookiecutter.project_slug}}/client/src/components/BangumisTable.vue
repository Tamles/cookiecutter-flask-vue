<template>
  <div>
    <a-table
      :columns="columns"
      :data-source="bangumis"
      :loading="loading"
      :pagination="pagination"
      bordered
      @change="handleTableChange"
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
              <a target="_blank" :href="text">
                <a-icon type="link" />
              </a>
            </div>
            <div v-else>{{ text }}</div>
          </template>
        </div>
      </template>
      <template slot="operation" slot-scope="text, record">
        <span v-if="record.editable">
          <a @click="() => save(record.key)"> <a-icon type="save" /></a>
          <a-popconfirm title="确定取消？" @confirm="() => cancel(record.key)">
            <a> <a-icon type="close" /></a>
          </a-popconfirm>
        </span>
        <span v-else>
          <a @click="() => edit(record.key)"> <a-icon type="edit" /></a>
        </span>
        <a-divider type="vertical" />
        <a-popconfirm
          v-if="bangumis.length"
          title="确定删除?"
          @confirm="() => onDelete(record.key)"
        >
          <a href="javascript:;"> <a-icon type="delete" /></a>
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
import BangumiCreationForm from '@/components/BangumiCreationForm'
import { createBangumi, retrieveBangumis, updateBangumi, deleteBangumi } from '@/apis/bangumi'
import moment from 'moment'
import _ from 'lodash'

const columns = [
  {
    title: '番剧名',
    dataIndex: 'name',
    scopedSlots: { customRender: 'name' }
  },
  {
    title: '上映时间',
    dataIndex: 'time',
    scopedSlots: { customRender: 'time' }
  },
  {
    title: '链接',
    dataIndex: 'url',
    scopedSlots: { customRender: 'url' }
  },
  {
    title: '操作',
    dataIndex: 'operation',
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'BangumisTable',
  components: {
    BangumiCreationForm
  },
  data() {
    return {
      columns,
      bangumis: [],
      cacheData: [],
      visible: false,
      loading: false,
      pagination: {}
    }
  },
  mounted() {
    this.fetch()
  },
  methods: {
    fetch(params = {}) {
      this.loading = true
      retrieveBangumis(params)
        .then(res => {
          this.loading = false
          this.bangumis = res.data.results.map(bangumi => ({
            ...bangumi,
            key: bangumi.id
          }))
          this.pagination = {
            ...this.pagination,
            total: res.data.total,
            pageSize: res.data.page_size
          }
          this.cacheData = _.cloneDeep(this.bangumis)
        })
        .catch(err => {
          console.log(err)
        })
    },
    moment(date) {
      return moment(date)
    },
    showModal() {
      this.visible = true
    },
    handleCancel() {
      this.visible = false
    },
    handleCreate() {
      const form = this.$refs.bangumiForm.form
      form.validateFields((err, values) => {
        if (err) {
          return
        }
        createBangumi(values).then(res => {
          this.bangumis.push({ ...res.data, key: res.data.id })
        })
        form.resetFields()
        this.visible = false
      })
    },
    handleTableChange(pagination) {
      this.pagination = { ...this.pagination, current: pagination.current }
      this.fetch({
        page: pagination.current
      })
    },
    onDelete(key) {
      deleteBangumi(key)
        .then(() => {
          this.bangumis = this.bangumis.filter(item => item.key !== key)
        })
        .catch(err => {
          console.log(err)
        })
    },
    handleChange(value, key, column) {
      const bangumis = [...this.bangumis]
      const target = bangumis.find(item => item.key === key)
      if (target) {
        target[column] = value
      }
    },
    edit(key) {
      const bangumis = [...this.bangumis]
      const target = bangumis.find(item => item.key === key)
      if (target) {
        target.editable = true
        this.bangumis = bangumis
      }
    },
    save(key) {
      const bangumis = [...this.bangumis]
      const target = bangumis.find(item => item.key === key)
      if (target) {
        delete target.editable
        updateBangumi(key, target)
          .then(() => {
            this.cacheData = _.cloneDeep(this.bangumis)
            this.bangumis = bangumis
          })
          .catch(err => console.log(err))
      }
    },
    cancel(key) {
      const bangumis = [...this.bangumis]
      const target = bangumis.find(item => item.key === key)
      if (target) {
        delete target.editable
        Object.assign(target, this.cacheData.find(item => item.key === key))
        this.bangumis = bangumis
      }
    }
  }
}
</script>
