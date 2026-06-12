<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('update:modelValue', false)"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 sm:mx-0 sm:h-10 sm:w-10">
              <svg class="h-6 w-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left flex-1">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                创建新相册
              </h3>
              <div class="mt-4 space-y-4">
                <!-- 相册名称 -->
                <div>
                  <label for="albumName" class="block text-sm font-medium text-gray-700">相册名称</label>
                  <input
                    id="albumName"
                    v-model="formData.name"
                    type="text"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    placeholder="请输入相册名称"
                    required
                  >
                </div>

                <!-- 相册描述 -->
                <div>
                  <label for="albumDescription" class="block text-sm font-medium text-gray-700">相册描述（可选）</label>
                  <textarea
                    id="albumDescription"
                    v-model="formData.description"
                    rows="3"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    placeholder="描述这个相册的内容和主题..."
                  ></textarea>
                </div>

                <!-- 相册类型 -->
                <div>
                  <label for="albumType" class="block text-sm font-medium text-gray-700">相册类型</label>
                  <select
                    id="albumType"
                    v-model="formData.albumType"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="normal">普通相册</option>
                    <option value="couple">情侣相册</option>
                    <option value="collaborative">协作相册</option>
                    <option value="smart">智能相册</option>
                    <option value="template">模板相册</option>
                  </select>
                </div>

                <!-- 隐私设置 -->
                <div class="flex items-center">
                  <input
                    id="isPrivate"
                    v-model="formData.isPrivate"
                    type="checkbox"
                    class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  >
                  <label for="isPrivate" class="ml-2 block text-sm text-gray-700">
                    设为私密相册
                  </label>
                </div>

                <!-- 标签 -->
                <div>
                  <label for="tags" class="block text-sm font-medium text-gray-700">标签（可选）</label>
                  <input
                    id="tags"
                    v-model="tagsInput"
                    type="text"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    placeholder="输入标签，用逗号分隔"
                    @keyup.enter="addTag"
                  >
                  <div v-if="formData.tags.length > 0" class="mt-2 flex flex-wrap gap-2">
                    <span
                      v-for="tag in formData.tags"
                      :key="tag"
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                    >
                      {{ tag }}
                      <button
                        @click="removeTag(tag)"
                        class="ml-1 text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </span>
                  </div>
                </div>

                <!-- 错误提示 -->
                <div v-if="error" class="text-red-600 text-sm">
                  {{ error }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            type="button"
            @click="handleSubmit"
            :disabled="loading || !isFormValid"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
            {{ loading ? '创建中...' : '创建相册' }}
          </button>
          <button
            type="button"
            @click="$emit('update:modelValue', false)"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useAlbumStore } from '../stores/album'
import type { CreateAlbumForm } from '../types'

// Props
const props = defineProps<{
  modelValue: boolean
}>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'success': []
}>()

// 使用相册状态管理
const albumStore = useAlbumStore()

// 表单数据
const formData = ref<CreateAlbumForm>({
  name: '',
  description: '',
  isPrivate: false,
  albumType: 'normal',
  tags: []
})

// 状态
const loading = ref(false)
const error = ref('')
const tagsInput = ref('')

// 计算属性
const isFormValid = computed(() => {
  return formData.value.name.trim() !== ''
})

// 方法
const resetForm = () => {
  formData.value = {
    name: '',
    description: '',
    isPrivate: false,
    albumType: 'normal',
    tags: []
  }
  tagsInput.value = ''
  error.value = ''
}

const addTag = () => {
  const tag = tagsInput.value.trim()
  if (tag && !formData.value.tags.includes(tag)) {
    formData.value.tags.push(tag)
    tagsInput.value = ''
  }
}

const removeTag = (tag: string) => {
  const index = formData.value.tags.indexOf(tag)
  if (index > -1) {
    formData.value.tags.splice(index, 1)
  }
}

const handleSubmit = async () => {
  if (!isFormValid.value) {
    error.value = '请填写相册名称'
    return
  }

  try {
    loading.value = true
    error.value = ''

    await albumStore.createAlbum(formData.value)

    // 关闭模态框并重置表单
    emit('update:modelValue', false)
    emit('success')
    resetForm()

  } catch (err) {
    error.value = err instanceof Error ? err.message : '创建失败，请重试'
    console.error('Create album error:', err)
  } finally {
    loading.value = false
  }
}

// 监听标签输入
watch(tagsInput, (newValue) => {
  if (newValue.includes(',')) {
    const tags = newValue.split(',').map(tag => tag.trim()).filter(tag => tag)
    tags.forEach(tag => {
      if (tag && !formData.value.tags.includes(tag)) {
        formData.value.tags.push(tag)
      }
    })
    tagsInput.value = ''
  }
})

// 监听模态框显示状态
watch(() => props.modelValue, (newValue) => {
  if (newValue) {
    resetForm()
  }
})
</script>

<style scoped>
/* 模态框样式 */
</style>




