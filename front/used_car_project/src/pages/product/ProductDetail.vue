<template>
  <q-layout class="page-container page-background">
    <q-page class="common-container-1">
      <div class="main-container">

        <!-- 차량 이미지 영역 -->
        <div class="img-area">
          <div class="img-box">

            <!-- Left arrow button -->
            <button @click="prevImage" class="arrow-left"><i class="fa-solid fa-chevron-left fa-xl"></i></button>

            <!-- Main image -->
            <img :src="mainImg" alt="차량 이미지" />

            <!-- Right arrow button -->
            <button @click="nextImage" class="arrow-right"><i class="fa-solid fa-chevron-right fa-xl"></i></button>
          </div>

          <!-- 썸네일 이미지 영역 -->
          <div class="thumbnails-wrapper">
            <div class="thumbnails">
              <img
                v-for="(image, index) in result.img"
                :key="index"
                :src="image"
                @mouseover="changeMainImage(image)"
                class="thumbnail-image"
                :class="{ active: image === mainImg }"
              />
            </div>
          </div>


          <!-- 차량 정보 -->
          <div class="car-info">
            <div class="car-name">{{ result.name }}</div>
            <p>{{ result.year }} / {{ result.fuel }} / {{ result.distance }}</p>
            <div class="price-info">
              <span class="price">{{ result.price }} 만원</span>
              <div class="price-right">
                <div style="position: relative;">
                  <span class="month-fee">할부적용</span>
                  <i
                    class="fa-regular fa-circle-question"
                    @mouseover="showTooltip = true"
                    @mouseleave="showTooltip = false"
                  ></i>
                  <div v-if="showTooltip" class="tooltip">
                    선납금과 이자 미포함 비용으로 실제 조건은 이용 조건 및 신용도에 따라 달라질 수 있습니다.
                  </div>
                </div>
                <div>
                  <select class="month-select" v-model="selectedMonths">
                    <option :value="12">12개월</option>
                    <option :value="24">24개월</option>
                    <option :value="36">36개월</option>
                    <option :value="48">48개월</option>
                    <option :value="60">60개월</option>
                    <option :value="72">72개월</option>
                  </select>
                </div>
                <div>
                  <span class="monthly-payment">월 {{ calculatedPayment }} 만원</span>
                </div>
              </div>
            </div>
          </div>


          <!-- 차량 상세 정보 -->
          <div class="car-detail">
            <div class="detail-grid">
              <div class="detail-item">
                <div class="detail-title">차량번호</div>
                <div class="detail-value">{{ result.number }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">색상</div>
                <div class="detail-value">{{ result.color }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">연식</div>
                <div class="detail-value">{{ result.year }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">주행거리</div>
                <div class="detail-value">{{ result.distance }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">연료 / 변속기</div>
                <div class="detail-value">{{ result.fuel }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">세부모델</div>
                <div class="detail-value">{{ result.grade }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">사고유무</div>
                <div class="detail-value">{{ result.accident }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">압류 / 저당</div>
                <div class="detail-value">{{ result.seize }}</div>
              </div>
              <div class="detail-item">
                <div class="detail-title">세금미납</div>
                <div class="detail-value">{{ result.tax_unpaid }}</div>
              </div>
            </div>
          </div>

          <!-- 차량 옵션 -->
          <div class="car-option">
            <div class="option-box">
              <div class="option-title">
                외관
              </div>
              <div class="option-line">
                <div class="option-item" v-for="(item, idx) in result.out_options" :key="idx">
                  <div class="option-tf">
                    <!-- v-bind로 체크 여부를 결정하고 disabled로 비활성화 -->
                    <input
                      class="option-check"
                      type="checkbox"
                      v-model="result.o_out_options[idx]"
                      :disabled="true"
                    />
                  </div>
                  <div class="option-name">{{ item }}</div>
                </div>
              </div>
            </div>

            <div class="option-box">
              <div class="option-title">
                내장
              </div>
              <div class="option-line">
                <div class="option-item" v-for="(item, idx) in result.in_options" :key="idx">
                  <div class="option-tf">
                    <!-- v-bind로 체크 여부를 결정하고 disabled로 비활성화 -->
                    <input
                      class="option-check"
                      type="checkbox"
                      v-model="result.o_in_options[idx]"
                      :disabled="true"
                    />
                  </div>
                  <div class="option-name">{{ item }}</div>
                </div>
              </div>
            </div>

            <div class="option-box">
              <div class="option-title">
                안전
              </div>
              <div class="option-line">
                <div class="option-item" v-for="(item, idx) in result.safe_options" :key="idx">
                  <div class="option-tf">
                    <!-- v-bind로 체크 여부를 결정하고 disabled로 비활성화 -->
                    <input
                      class="option-check"
                      type="checkbox"
                      v-model="result.o_safe_options[idx]"
                      :disabled="true"
                    />
                  </div>
                  <div class="option-name">{{ item }}</div>
                </div>
              </div>
            </div>

            <div class="option-box">
              <div class="option-title">
                편의
              </div>
              <div class="option-line">
                <div class="option-item" v-for="(item, idx) in result.conv_options" :key="idx">
                  <div class="option-tf">
                    <!-- v-bind로 체크 여부를 결정하고 disabled로 비활성화 -->
                    <input
                      class="option-check"
                      type="checkbox"
                      v-model="result.o_conv_options[idx]"
                      :disabled="true"
                    />
                  </div>
                  <div class="option-name">{{ item }}</div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </q-page>
  </q-layout>
</template>

<script setup>
import { defineComponent, onMounted, ref, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { api } from "boot/axios";

// 기본 세팅
const $router = useRouter();
const $route = useRoute();

const result = ref({});
const mainImg = ref("");
const currentIndex = ref(0);

const selectedMonths = ref(12);
const showTooltip = ref(false);

// API 호출
const CarData = async (id) => {
  const url = `${process.env.API}products/${id}`;

  try {
    const res = await api.get(url);
    result.value = res.data;

    if (result.value.img.length > 0) {
      mainImg.value = result.value.main_img;
      console.log("mainImg 확인", mainImg.value);
      currentIndex.value = 0;
    }
    console.log("API 호출 결과 확인", result.value);
  } catch (err) {
    console.log(err);
  }
};


const changeMainImage = (image) => {
  mainImg.value = image;
  currentIndex.value = result.value.img.indexOf(image);
};


const prevImage = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    mainImg.value = result.value.img[currentIndex.value];
  }
};


const nextImage = () => {
  if (currentIndex.value < result.value.img.length - 1) {
    currentIndex.value++;
    mainImg.value = result.value.img[currentIndex.value];
  }
};

const calculatedPayment = computed(() => {
  const payment = Math.ceil(result.value.price_unit / selectedMonths.value / 10000); // 만원 단위로 나누고 올림 처리
  return payment; // 계산된 할부금
});

onMounted(() => {
  CarData($route.params.id);
});
</script>

<style scoped>
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 20px;
  max-width: 100%;
  overflow: hidden;
}

.img-box {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

img {
  max-width: 100%;
  height: auto;
}

.thumbnails-wrapper {
  max-width: 100%;
  overflow-x: auto;
  white-space: nowrap;
}

.thumbnails {
  /* display: flex; */
  justify-content: center;
  gap: 10px;
}

.thumbnail-image {
  width: 100px;
  height: auto;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.3s;
}

.thumbnail-image.active {
  border-color: #3498db;
}

.arrow-left,
.arrow-right {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  /* background-color: rgba(0, 0, 0, 0.5); */
  color: black;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.arrow-left {
  left: 0px;
}

.arrow-right {
  right: 0px;
}
.img-area {
    background-color: #ffff;
    border-radius: 20px;
    padding: 10px;
}

.car-info {
  padding: 20px;
}

.price-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: #e74c3c;
}

.monthly-payment {
  font-size: 16px;
  color: #7f8c8d;
}
.car-name {
    font-size: 28px;
    font-weight: bold;
}

.car-detail {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
  /* background-color: #f9f9f9; */
  border-radius: 10px;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 15px;
}

.detail-item {
  background-color: #fff;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.detail-title {
  font-size: 14px;
  color: #5f696a;
  margin-bottom: 5px;
}

.detail-value {
  font-size: 16px;
  font-weight: bold;
  color: #2c3e50;
}

.car-option {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
  }

  .option-line {
    padding-top: 15px;
  }

  .option-item {
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 2px;
  }

  .option-tf {
    display: flex;
    align-items: center;
  }

  .option-check {
    /* 크기 키우기 */
    transform: scale(1);
    /* 커스터마이즈된 색상 */
    appearance: none;
    width: 20px;
    height: 20px;
    border: 2px solid #f21536;
    border-radius: 3px;
    outline: none;
    background-color: white;
    cursor: not-allowed;
  }

  /* 체크박스가 체크된 경우의 스타일 */
  .option-check:checked {
    background-color: #f21536;
    border-color: #f21536;
    position: relative;
  }

  /* 체크박스 내부 체크 표시 */
  .option-check:checked::after {
    content: '';
    position: absolute;
    top: 2px;
    left: 5px;
    width: 6px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
  }

  .option-name {
    font-size: 14px;
  }
  .car-info {
  padding: 20px;
}

.price-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.price {
  font-size: 24px;
  font-weight: bold;
  color: #f21536;
}

.monthly-payment {
  font-size: 15px;
  color: #7f8c8d;
}


.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background-color: black;
  color: white;
  padding: 5px;
  border-radius: 5px;
  width: 300px;
  text-align: center;
  visibility: visible;
  opacity: 1;
  transition: opacity 0.3s ease;
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: black transparent transparent transparent;
}

.price-right {
  display: flex;
  gap: 7px;
}

.month-fee {
  font-size: 15px;
}

.fa-circle-question {
  font-size: 16px;
    color: #bbb7b7;
    margin-left: 5px;
}
.month-select{
  font-size: 15px;
  border: 2px solid #bbb7b7;
  border-radius: 3px;
}
.option-title{
  font-size: 16px;
    font-weight: bold;
    color: #2c3e50;
}
</style>
