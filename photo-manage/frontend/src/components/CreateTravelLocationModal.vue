<template>
  <div v-if="modelValue" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('update:modelValue', false)"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-green-100 sm:mx-0 sm:h-10 sm:w-10">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
              </svg>
            </div>
            <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left flex-1">
              <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                添加旅行地点
              </h3>
              <div class="mt-4 space-y-4">
                <!-- 省份城市选择 -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="province" class="block text-sm font-medium text-gray-700">省份</label>
                    <select
                      id="province"
                      v-model="formData.province"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      required
                    >
                      <option value="">选择省份</option>
                      <option value="云南">云南</option>
                      <option value="北京">北京</option>
                      <option value="浙江">浙江</option>
                      <option value="上海">上海</option>
                      <option value="广东">广东</option>
                      <option value="四川">四川</option>
                      <option value="江苏">江苏</option>
                      <option value="湖南">湖南</option>
                      <option value="山东">山东</option>
                    </select>
                  </div>
                  <div>
                    <label for="city" class="block text-sm font-medium text-gray-700">城市</label>
                    <input
                      id="city"
                      v-model="formData.city"
                      type="text"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="请输入城市"
                      required
                    >
                  </div>
                </div>

                <!-- 区县和地点名称 -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="district" class="block text-sm font-medium text-gray-700">区县（可选）</label>
                    <input
                      id="district"
                      v-model="formData.district"
                      type="text"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="请输入区县"
                    >
                  </div>
                  <div>
                    <label for="locationName" class="block text-sm font-medium text-gray-700">地点名称（可选）</label>
                    <input
                      id="locationName"
                      v-model="formData.locationName"
                      type="text"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="如：西湖、故宫等"
                    >
                  </div>
                </div>

                <!-- 描述 -->
                <div>
                  <label for="description" class="block text-sm font-medium text-gray-700">地点描述（可选）</label>
                  <textarea
                    id="description"
                    v-model="formData.description"
                    rows="3"
                    class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                    placeholder="描述这个地方的特点、感受等..."
                  ></textarea>
                </div>

                <!-- 坐标信息（可选） -->
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label for="latitude" class="block text-sm font-medium text-gray-700">纬度（可选）</label>
                    <input
                      id="latitude"
                      v-model="formData.latitude"
                      type="number"
                      step="0.000001"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="如：30.2592"
                    >
                  </div>
                  <div>
                    <label for="longitude" class="block text-sm font-medium text-gray-700">经度（可选）</label>
                    <input
                      id="longitude"
                      v-model="formData.longitude"
                      type="number"
                      step="0.000001"
                      class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500"
                      placeholder="如：120.1316"
                    >
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
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
            {{ loading ? '创建中...' : '创建地点' }}
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
import { useTravelStore } from '../stores/travel'

// Props
const props = defineProps<{
  modelValue: boolean
}>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'success': []
}>()

// 使用旅行状态管理
const travelStore = useTravelStore()

// 表单数据
const formData = ref({
  province: '',
  city: '',
  district: '',
  locationName: '',
  description: '',
  latitude: null as number | null,
  longitude: null as number | null
})

// 状态
const loading = ref(false)
const error = ref('')

// 计算属性
const isFormValid = computed(() => {
  return formData.value.province.trim() !== '' &&
         formData.value.city.trim() !== ''
})

// 方法
const resetForm = () => {
  formData.value = {
    province: '',
    city: '',
    district: '',
    locationName: '',
    description: '',
    latitude: null,
    longitude: null
  }
  error.value = ''
}

const handleSubmit = async () => {
  if (!isFormValid.value) {
    error.value = '请填写必需的省份和城市信息'
    return
  }

  try {
    loading.value = true
    error.value = ''

    // 检查是否已存在相同的地点
    const existingLocation = travelStore.locations.find(loc =>
      loc.province === formData.value.province &&
      loc.city === formData.value.city &&
      (!formData.value.district || loc.district === formData.value.district)
    )

    if (existingLocation) {
      error.value = '该地点已存在，请勿重复添加'
      return
    }

    // 创建新地点
    await travelStore.createLocation({
      province: formData.value.province,
      city: formData.value.city,
      district: formData.value.district || undefined,
      locationName: formData.value.locationName || undefined,
      description: formData.value.description || undefined,
      latitude: formData.value.latitude || undefined,
      longitude: formData.value.longitude || undefined,
      isFavorite: false
    })

    // 关闭模态框并重置表单
    emit('update:modelValue', false)
    emit('success')
    resetForm()

  } catch (err) {
    error.value = err instanceof Error ? err.message : '创建失败，请重试'
    console.error('Create location error:', err)
  } finally {
    loading.value = false
  }
}

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




