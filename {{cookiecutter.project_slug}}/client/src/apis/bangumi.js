import request from '@/utils/request'

export function createBangumi(data) {
  return request({
    url: '/bangumis',
    method: 'post',
    data
  })
}

export function retrieveBangumis(query) {
  return request({
    url: '/bangumis',
    method: 'get',
    params: query
  })
}

export function updateBangumi(id, data) {
  return request({
    url: `/bangumis/${id}`,
    method: 'put',
    data
  })
}

export function deleteBangumi(id) {
  return request({
    url: `/bangumis/${id}`,
    method: 'delete'
  })
}
