<template>
  <q-layout class="page-container page-background">
    <q-page class="common-container-1">
      <div class="main-container">
        <!-- 검색창 영역 -->
        <div class="search-bar">
          <div class="se-top">
            <div class="se-title">
              국산차 검색
            </div>
            <div class="se-quan">
              {{domesticProductCount}}대
            </div>
          </div>

          <div class="se-middle">
            <div class="reset-btn" @click="resetAll()">
              <i class="fa-solid fa-rotate-right"></i>선택초기화
            </div>
            <div class="recent-search-btn" @click="toggleRecentSearch">
              <i class="fa-solid fa-magnifying-glass"></i>최근 검색조건
            </div>
          </div>

          <!-- 최근 검색조건 목록 -->
          <div v-if="isRecentSearchOpen" class="recent-search-list">
            <div class="recent-search-items">
              <!-- 최근 검색 조건을 한 줄로 나열 -->
              <div class="recent-cont" v-for="(condition, index) in recentSearchCondition" :key="index">
                {{ condition.manufacturer }} {{ condition.model }} <div class="delete-btn">삭제</div>
              </div>
            </div>
            <button @click="clearRecentSearches()">최근 검색조건 초기화</button>
          </div>


          <!-- 차종 선택 영역 -->
          <div class="filter-section">
            <div @click="toggleCarTypeDropdown" class="dropdown-header">
              차종
              <i :class="isCarTypeDropdownOpen ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"></i>
            </div>
            <div v-if="isCarTypeDropdownOpen" class="dropdown-body">
              <div class="checkbox-container" v-for="(type, index) in carTypes" :key="index">
                <label class="checkbox-label">
                  <div> <input type="checkbox" :value="type" v-model="selectedCarTypes" class="custom-checkbox" /></div>
                  {{ type }}

                </label>
              </div>
            </div>
          </div>


          <!-- 제조사/모델/등급 선택영역 -->
          <div class="filter-section">
            <div class="dropdown-header">
              제조사/모델/등급
            </div>

            <!-- 선택된 제조사 상단에 표시 -->
            <div v-if="selectedManufacturer" class="selected-manufacturer">
              <span>{{ selectedManufacturer }}</span>
              <button class="del-btn" @click="clearSelectedManufacturer">X</button>
            </div>
            <div v-if="selectedModel" class="selected-manufacturer">
              <span>{{ selectedModel }}</span>
              <button class="del-btn" @click="clearSelectedModel">X</button>
            </div>
            <div v-if="selectedDetailModel" class="selected-manufacturer">
              <span>{{ selectedDetailModel }}</span>
              <button class="del-btn" @click="clearSelectedDetailModel">X</button>
            </div>

            <div class="dropdown-body">
              <!-- 제조사 목록 -->
              <div class="manufacturer-list">
                <div
                  v-for="(maker, index) in filteredManufacturers"
                  :key="index"
                  class="manufacturer-item"
                  @click="toggleManufacturer(maker)"
                >
                  {{ maker }}

                  <!-- 선택된 제조사의 모델 목록 -->
                  <div v-if="openManufacturer === maker" class="model-list">
                    <div
                      v-for="(model, modelIndex) in filteredModels"
                      :key="modelIndex"
                      class="model-item"
                      @click.stop="toggleModel(model)"
                    >
                      {{ model }}

                      <!-- 선택된 모델의 세부모델 목록 -->
                      <div v-if="openModel === model" class="detail-model-list">
                        <div
                          v-for="(item, detailIndex) in detailModelsBymodels[model]"
                          :key="detailIndex"
                          class="detail-model-item"
                          @click.stop="toggleDetailModel(item)"
                        >
                          {{ item }}
                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>



          <!-- 연식 선택 영역 -->
          <div class="filter-section">
            <div @click="toggleYearDropdown" class="dropdown-header">
              연식
              <i :class="isYearDropdownOpen ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"></i>
            </div>
            <div v-if="isYearDropdownOpen" class="dropdown-body">
              <div class="year-selection">
                <!-- 시작 연식 선택 -->
                <q-select
                  v-model="startYear"
                  :options="yearOptions"
                  label="시작 연도"
                  filled
                  stack-label

                ></q-select>

                <!-- 종료 연식 선택 -->
                <q-select
                  v-model="endYear"
                  :options="filteredYearOptions"
                  label="종료 연도"
                  filled
                  stack-label
                ></q-select>
              </div>
            </div>
          </div>
           <!-- 주행거리 선택 영역 -->
            <div class="filter-section">
              <div @click="toggleDistanceDropdown" class="dropdown-header">
                주행거리
                <i :class="isDistanceDropdownOpen ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"></i>
              </div>
              <div v-if="isDistanceDropdownOpen" class="dropdown-body">
                <div class="distance-selection">
                  <!-- 최소 주행거리 선택 -->
                  <q-select
                    v-model="minDistanceDisplay"
                    :options="formattedDistanceOptions"
                    label="최소 주행거리"
                    filled
                    stack-label
                  ></q-select>

                  <!-- 최대 주행거리 선택 -->
                  <q-select
                    v-model="maxDistanceDisplay"
                    :options="formattedDistanceOptions"
                    label="최대 주행거리"
                    filled
                    stack-label
                  ></q-select>
                </div>
              </div>
            </div>

            <!-- 가격 선택 영역 -->
            <div class="filter-section">
              <div @click="togglePriceDropdown" class="dropdown-header">
                가격
                <i :class="isPriceDropdownOpen ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"></i>
              </div>
              <div v-if="isPriceDropdownOpen" class="dropdown-body">
                <div class="price-selection">
                  <!-- 최소 가격 선택 -->
                  <q-select
                    v-model="minPrice"
                    :options="priceOptions"
                    label="최소 검색 가격"
                    filled
                    stack-label
                  ></q-select>

                  <!-- 최대 가격 선택 -->
                  <q-select
                    v-model="maxPrice"
                    :options="priceOptions"
                    label="최대 검색 가격"
                    filled
                    stack-label
                  ></q-select>
                </div>
              </div>
            </div>

        </div>
        <div v-if="NoResult" class="no-result">검색결과가 없습니다.</div>
        <!-- 상품 리스트 영역 -->
        <div class="item-area" v-else>

          <!-- <div>검색결과가 없습니다.</div> -->

          <!-- 상품 리스트 데이터 로딩 후 렌더링할 공간 -->
          <div
             v-for="(product, index) in result.products"
            :key="index"
            class="pro-box"
            @click="goDetail(product.id)"
          >
          <div class="pro-img-wrapper">
            <img  :src="product.img[0]" class="pro-img" alt="상품 이미지" />
            <button
              v-if="!isInterestProduct(product.id)"
              class="bookmark-btn"
              @click.stop="createInterestProduct(product.id)"
            >
              관심등록
            </button>
            <div v-if="isInterestProduct(product.id)" class="interest-badge">관심상품</div> <!-- 관심상품 표시 -->
          </div>
            <div class="pro-info">
              <div class="pro-title">{{ product.name }}</div>
              <div class="pro-details">
                <span class="pro-year">{{ product.year }}</span>
                <span class="pro-separator">|</span>
                <span class="pro-mileage">{{ product.distance }}</span>
              </div>
              <div class="pro-details">
                <span class="pro-year">{{ product.fuel }}</span>
              </div>
              <div class="pro-price"><span class="price-text">{{ product.price }}</span>만원</div>
              <div class="pro-details-2">
                <span class="pro-sub1" v-if="product.is_home">TRUST CAR홈서비스</span>
                <span class="pro-sub2" v-if="product.is_assurance">TRUST CAR보증</span>
              </div>
            </div>
          </div>

          <div class="page-box">
            <q-pagination
              v-model="currentPage"
              :max="maxPages"
              boundary-links
              max-pages="5"
              color="red-6"
              @update:model-value="changePage"
              class="custom-pagination"
            />
          </div>

        </div>






      </div>
    </q-page>
  </q-layout>
</template>

<script setup>
import { defineComponent, onBeforeMount, onMounted, ref, computed, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useQuasar } from "quasar";
import { api } from "boot/axios";
import axios from "axios";

defineOptions({
  name: "ProductList",
});

// 기본 세팅
const $router = useRouter();
const route = useRoute();
const $q = useQuasar();
let isInitialLoad = true;  // 초기 로딩을 확인하는 플래그

// 상태 관리
const isCarTypeDropdownOpen = ref(false);
const isYearDropdownOpen = ref(false);
const isDistanceDropdownOpen = ref(false);
const isPriceDropdownOpen = ref(false);
const isRecentSearchOpen = ref(false);


// 차종 및 제조사 목록
const carTypes = ["경차", "소형차", "준중형차", "중형차", "대형차", "스포츠카", "SUV", "RV"];
const selectedCarTypes = ref([]);
const manufacturers = ["현대", "제네시스", "기아", "쉐보레(GM대우)", "르노코리아(삼성)", "KG모빌리티(쌍용)"];
const modelsByManufacturer = ref({
  "현대": [
    "그랜저", "아반떼", "쏘나타", "싼타페", "스타렉스", "투싼", "펠리세이드", "제네시스",
    "코나", "에쿠스", "스타리아", "캐스퍼", "아이오닉5", "엑센트", "i30", "벨로스터",
    "맥스크루즈", "베뉴", "아이오닉", "i40", "베라크루즈", "넥쏘", "쏠라티", "아슬란", "아이오닉6"
  ],
  "제네시스": ["G70", "G80", "G90", "GV70", "GV80", "GV90"],
  "기아": ["카니발","쏘렌토","K5","모닝","레이","K7","스포티지","K3","K8","모하비","셀토스","K9","니로","쏘울","스팅어","EV6","프라이드","포르테","스토닉","카렌스","오피러스","로체","EV9","EV3","엔터프라이즈"],
  "쉐보레(GM대우)": ["스파크","말리부","트랙스","크루즈","올란도","트레일블레이저","마티즈","알페온","볼트EV","아쿼녹스","다마스","임팔라","캡티바","콜로라도","아베오","라보","트래버스","라세티","카마로","볼트EUV","타호","토스카","볼트","윈스톰","티코"],
  "르노코리아(삼성)":["QM6","SM6","SM5","SM3","XM3","SM7","QM3","QM5","마스터","조에","클리오","캡처","트위지","아르카나"],
  "KG모빌리티(쌍용)":["티볼리","렉스턴","코란도","토레스","체어맨","엑티언","무쏘","카이런","로디우스","이스타나","뉴훼미리","칼리스타"]
});
const detailModelsBymodels = ref({
  "그랜저": [
    "그랜저 (GN7) (22년~현재)",
    "그랜저 하이브리드 (GN7) (22년~현재)",
    "더 뉴 그랜저 IG (19년~22년)",
    "더 뉴 그랜저 IG 하이브리드 (19년~22년)",
    "그랜저 IG 하이브리드 (17년~19년)",
    "그랜저 IG (16년~19년)",
    "그랜저 HG 하이브리드 (13년~17년)",
    "그랜저 HG (11년~16년)",
    "더 럭셔리 그랜저 (09년~11년)",
    "그랜저 뉴 럭셔리 (08년~09년)"
  ],
  "아반떼": [
    "더 뉴 아반떼 (CN7) (23년~현재)",
    "더 뉴 아반떼 하이브리드 (CN7) (23년~현재)",
    "아반떼 하이브리드 (CN7) (20년~23년)",
    "아반떼 (CN7) (20년~23년)",
    "더 뉴 아반떼 AD (18년~20년)",
    "아반떼 AD (15년~18년)",
    "더 뉴 아반떼 (13년~15년)",
    "아반떼 쿠페 (13년~15년)",
    "아반떼 MD (10년~13년)",
    "아반떼 하이브리드 (09년~13년)",
    "아반떼 HD (06년~10년)",
    "뉴 아반떼 XD (03년~06년)",
    "아반떼 XD (00년~03년)",
    "올 뉴 아반떼 (98년~00년)",
    "아반떼 (95년~98년)"
  ],
  "쏘나타":[
    "쏘나타 디 엣지(DN8) (23년~현재)",
    "쏘나타 디 엣지 하이브리드(DN8) (23년~현재)",
    "쏘나타 하이브리드 (DN8) (19년~23년)",
    "쏘나타 (DN8) (19년~23년)",
    "쏘나타 뉴 라이즈 하이브리드 (17년~19년)",
    "쏘나타 뉴 라이즈 (17년~19년)",
    "LF 쏘나타 하이브리드 (14년~17년)",
    "LF 쏘나타 (14년~17년)",
    "쏘나타 더 브릴리언트 (12년~14년)",
    "쏘나타 하이브리드 (11년~14년)",
    "YF 쏘나타 (09년~12년)",
    "NF 쏘나타 트랜스폼 (07년~13년)"
  ],"싼타페":[
    "싼타페 (MX5) (23년~현재)",
    "더 뉴 싼타페 (20년~23년)",
    "싼타페 TM (18년~20년)",
    "싼타페 더 프라임 (15년~18년)",
    "싼타페 DM (12년~15년)",
    "싼타페 CM (05년~12년)",
    "싼타페 (00년~05년)"
  ],
  "스타렉스":[
    "더 뉴 그랜드 스타렉스 (17년~21년)",
    "그랜드 스타렉스 (07년~17년)",
    "스타렉스 점보 (97년~07년)",
    "스타렉스 (97년~07년)"
  ],
  "투싼":[
  "더 뉴 투싼 (NX4) (23년~현재)",
  "더 뉴 투싼 하이브리드 (NX4) (23년~현재)",
  "투싼 (NX4) (20년~23년)",
  "투싼 하이브리드 (NX4) (20년~23년)",
  "올 뉴 투싼 (15년~20년)",
  "뉴 투싼 ix (13년~15년)",
  "투싼 ix (09년~13년)",
  "투싼 (04년~09년)"
  ],
  "펠리세이드":[
    "더 뉴 펠리세이드(22년~현재)",
    "펠리세이드(18년~22년)"
  ],
  "제네시스":[
    "제네시스 DH(13년~16년)",
    "더 뉴 제네시스 쿠페(11년~16년)",
    "제네시스 쿠페(08년~11년)",
    "제네시스(08년~13년)"
  ],
  "코나":[
  "코나 일렉트릭 (SX2) (23년~현재)",
  "코나 (SX2) (23년~현재)",
  "코나 하이브리드 (SX2) (23년~현재)",
  "더 뉴 코나 (20년~23년)",
  "더 뉴 코나 하이브리드 (20년~23년)",
  "코나 하이브리드 (19년~20년)",
  "코나 일렉트릭 (18년~23년)",
  "코나 (17년~20년)"
  ],
  "에쿠스":[
    "에쿠스(신형)(09년~15년)",
    "에쿠스(99년~09년)"
  ],
  "스타리아":[
    "스타리아(21년~현재)"
  ],
  "캐스퍼":[
    "캐스퍼(21년~현재)"
  ],
  "아이오닉5":[
    "더 뉴 아이오닉5(24년~현재)",
    "아이오닉5(21년~24년)"
  ],
  "엑센트":[
    "엑센트(신형)(10년~19년)",
    "뉴 엑센트(97년~99년)",
    "엑센트(94년~97년)"
  ],
  "i30":[
    "i30 (PD) (16년~20년)",
    "더 뉴 i30 (15년~16년)",
    "i30(신형) (11년~15년)",
    "i30 cw (08년~11년)",
    "i30 (07년~11년)"
  ],
  "벨로스터":[
    "벨로스터 (JS) (18년~22년)",
    "더 뉴 벨로스터 (15년~18년)",
    "벨로스터 (11년~14년)"
  ],
  "맥스크루즈":[
    "더 뉴 맥스크루즈(15년~19년)",
    "맥스크루즈(13년~15년)"
  ],
  "베뉴":[
    "베뉴(19년~현재)"
  ],
  "아이오닉":[
    "더 뉴 아이오닉 일렉트릭(19년~21년)",
    "더 뉴 아이오닉 하이브리드(19년~21년)",
    "아이오닉 일렉트릭(16년~19년)",
    "아이오닉 하이브리드(16년~19년)"
  ],
  "i40":[
    "더 뉴 i40 (15년~19년)",
    "더 뉴 i40 살룬 (15년~19년)",
    "i40 살룬 (12년~15년)",
    "i40 (11년~15년)"
  ],
  "베라크루즈":[
    "베라크루즈(06년~15년)"
  ],
  "넥쏘":[
    "넥쏘(18년~현재)"
  ],
  "쏠라티":[
    "쏠라티(20년~현재)"
  ],
  "아슬란":[
    "아슬란(14년~18년)"
  ],
  "아이오닉6":[
    "아이오닉6(22년~현재)"
  ],
  "G80": [
    "일렉트리파이드 G80 (RG3) (21년~현재)",
    "G80 (RG3) (20년~현재)",
    "G80 (16년~20년)"
  ],

  "GV70": [
    "일렉트리파이드 GV70 (22년~현재)",
    "GV70 (21년~현재)"
  ],

  "G70": [
    "더 뉴 G70 슈팅브레이크 (22년~현재)",
    "더 뉴 G70 (20년~현재)",
    "G70 (17년~20년)"
  ],

  "G90": [
    "G90 (RS4) (21년~현재)",
    "G90 (18년~21년)"
  ],

  "GV60": [
    "GV60 (21년~현재)"
  ],

  "GV80": [
    "GV80 쿠페 (23년~현재)",
    "GV80 (20년~현재)"
  ],
  "EQ900":[
    "EQ900(15년~18년)"
  ],
  "카니발": [
    "더 뉴 카니발 4세대 (23년~현재)",
    "카니발 4세대 (20년~23년)",
    "더 뉴 카니발 (18년~20년)",
    "올 뉴 카니발 (14년~18년)",
    "카니발 R (10년~14년)",
    "뉴카니발 (06년~10년)",
    "그랜드 카니발 (05년~10년)",
    "카니발 II (01년~05년)",
    "카니발 (98년~01년)"
  ],

  "K3": [
    "더 뉴 K3 2세대 (21년~현재)",
    "올 뉴 K3 (18년~21년)",
    "더 뉴 K3 쿱 (16년~17년)",
    "더 뉴 K3 유로 (16년~18년)",
    "더 뉴 K3 (15년~18년)",
    "K3 유로 (13년~16년)",
    "K3 쿱 (13년~16년)",
    "K3 (12년~15년)"
  ],

  "K5": [
    "더 뉴 K5 3세대 (23년~현재)",
    "더 뉴 K5 하이브리드 3세대 (23년~현재)",
    "K5 3세대 (19년~23년)",
    "K5 하이브리드 3세대 (19년~23년)",
    "더 뉴 K5 하이브리드 2세대 (18년~19년)",
    "더 뉴 K5 2세대 (18년~19년)",
    "K5 하이브리드 2세대 (15년~18년)",
    "K5 2세대 (15년~18년)",
    "더 뉴 K5 (13년~15년)",
    "K5 하이브리드 (11년~15년)",
    "K5 (10년~13년)"
  ],

  "K7": [
    "K7 프리미어 (19년~21년)",
    "K7 프리미어 하이브리드 (19년~21년)",
    "올 뉴 K7 하이브리드 (16년~19년)",
    "올 뉴 K7 (16년~19년)",
    "K7 하이브리드 (13년~16년)",
    "더 뉴 K7 (12년~16년)",
    "더 프레스티지 K7 (11년~12년)",
    "K7 (09년~11년)"
  ],

  "K8": [
    "K8 (21년~현재)",
    "K8 하이브리드 (21년~현재)"
  ],

  "K9": [
    "더 뉴 K9 2세대 (21년~현재)",
    "더 K9 (18년~21년)",
    "더 뉴 K9 (14년~18년)",
    "K9 (12년~14년)"
  ],

  "EV3": [
    "EV3 (24년~현재)"
  ],

  "EV6": [
    "더 뉴 EV6 (24년~현재)",
    "EV6 (21년~24년)"
  ],

  "EV9": [
    "EV9 (23년~현재)"
  ],

  "쏘렌토": [
    "더 뉴 쏘렌토 4세대 (23년~현재)",
    "쏘렌토 4세대 (20년~23년)",
    "더 뉴 쏘렌토 (17년~20년)",
    "올 뉴 쏘렌토 (14년~17년)",
    "뉴 쏘렌토 R (12년~14년)",
    "쏘렌토 R (09년~12년)",
    "뉴쏘렌토 (06년~09년)",
    "쏘렌토 (02년~06년)"
  ],

  "모닝": [
    "더 뉴 모닝 (JA) (23년~현재)",
    "모닝 어반 (JA) (20년~23년)",
    "올 뉴 모닝 (JA) (17년~20년)",
    "더 뉴 모닝 (15년~17년)",
    "올 뉴 모닝 (11년~15년)",
    "뉴모닝 (08년~11년)",
    "모닝 (04년~08년)"
  ],

  "레이": [
    "더 뉴 기아 레이 EV (23년~현재)",
    "더 뉴 기아 레이 (22년~현재)",
    "더 뉴 레이 (17년~22년)",
    "레이 (11년~17년)"
  ],

  "스포티지": [
    "스포티지 5세대 (21년~현재)",
    "스포티지 5세대 하이브리드 (21년~현재)",
    "스포티지 더 볼드 (18년~21년)",
    "스포티지 4세대 (15년~18년)",
    "더 뉴 스포티지 R (13년~15년)",
    "스포티지 R (10년~13년)",
    "New 스포티지 (04년~10년)",
    "스포티지 (93년~02년)"
  ],

  "모하비": [
    "모하비 더 마스터 (19년~현재)",
    "더 뉴 모하비 (16년~19년)",
    "모하비 (07년~16년)"
  ],

  셀토스: [
    "더 뉴 셀토스 (22년~현재)",
    "셀토스 (19년~22년)"
  ],

  니로: [
    "디 올 뉴 니로 EV (22년~현재)",
    "니로 플러스 (22년~현재)",
    "디 올 뉴 니로 (22년~현재)",
    "더 뉴 니로 (19년~22년)",
    "니로 EV (18년~22년)",
    "니로 (16년~19년)"
  ],

  "쏘울": [
    "쏘울 부스터 EV (19년~21년)",
    "쏘울 부스터 (19년~21년)",
    "더 뉴 쏘울 (16년~19년)",
    "쏘울 EV (14년~19년)",
    "올 뉴 쏘울 (13년~16년)",
    "쏘울 (08년~13년)"
  ],

  "스팅어": [
    "스팅어 마이스터 (20년~현재)",
    "스팅어 (17년~20년)"
  ],

  "프라이드": [
    "더 뉴 프라이드 (15년~17년)",
    "올 뉴 프라이드 (11년~15년)",
    "프라이드(신형) (05년~11년)",
    "프라이드 (87년~00년)"
  ],

  "포르테": [
    "포르테 해치백 (10년~13년)",
    "포르테 쿱 (09년~13년)",
    "포르테 (08년~13년)"
  ],

  "스토닉": [
    "스토닉 (17년~20년)"
  ],

  "카렌스": [
    "더 뉴 카렌스 (16년~18년)",
    "올 뉴 카렌스 (13년~16년)",
    "뉴카렌스 (06년~13년)",
    "카렌스 II (02년~06년)",
    "카렌스 (99년~02년)"
  ],

  "오피러스": [
    "오피러스 프리미엄 (09년~11년)",
    "뉴오피러스 (06년~09년)",
    "오피러스 (03년~06년)"
  ],

  "로체": [
    "로체 이노베이션 (08년~10년)",
    "로체 어드밴스 (07년~08년)",
    "로체 (05년~07년)"
  ],

  "엔터프라이즈": [
    "엔터프라이즈 (97년~02년)"
  ],
  "스파크": [
    "더 뉴 스파크 (18년~23년)",
    "더 넥스트 스파크 (15년~18년)",
    "스파크 EV (13년~16년)",
    "스파크 (11년~15년)"
  ],
  "말리부": [
    "더 뉴 말리부 (18년~23년)",
    "올 뉴 말리부 (16년~18년)",
    "말리부 (11년~16년)"
  ],
  "트랙스": [
    "트랙스 크로스오버 (23년~현재)",
    "더 뉴 트랙스 (16년~22년)",
    "트랙스 (13년~16년)"
  ],
  "크루즈": [
    "올 뉴 크루즈 (17년~18년)",
    "어메이징 뉴 크루즈 (15년~17년)",
    "어메이징 뉴 크루즈5 (15년~17년)",
    "크루즈5 (11년~14년)",
    "크루즈 (11년~14년)"
  ],
  "올란도": [
    "올란도 (11년~18년)"
  ],
  "트레일블레이저": [
    "더 뉴 트레일블레이저 (23년~현재)",
    "트레일블레이저 (20년~23년)"
  ],
  "마티즈": [
    "마티즈 크리에이티브 (09년~11년)",
    "마티즈 클래식 (09년~11년)",
    "All New 마티즈 (05년~09년)",
    "마티즈 II (00년~05년)",
    "마티즈 (98년~00년)"
  ],
  "알페온": [
    "알페온 (10년~15년)"
  ],
  "볼트EV": [
    "뉴 볼트 EV (21년~23년)",
    "볼트 EV (17년~21년)"
  ],
  "아쿼녹스": [
    "더 넥스트 이쿼녹스 (22년~현재)",
    "이쿼녹스 (18년~20년)"
  ],
  "다마스": [
    "뉴 다마스 (08년~21년)",
    "다마스 II (03년~07년)",
    "다마스 (91년~03년)"
  ],
  "임팔라": [
    "임팔라 (15년~20년)"
  ],
  "캡티바": [
    "캡티바 (11년~18년)"
  ],
  "콜로라도": [
    "올 뉴 콜로라도 (24년~현재)",
    "리얼 뉴 콜로라도 (20년~24년)",
    "콜로라도 (19년~20년)"
  ],
  "아베오": [
    "더 뉴 아베오 세단 (16년~19년)",
    "더 뉴 아베오 해치백 (16년~19년)",
    "아베오 세단 (11년~16년)",
    "아베오 해치백 (11년~16년)"
  ],
  "라보": [
    "뉴 라보 (08년~21년)",
    "라보 (91년~06년)"
  ],
  "트래버스": [
    "트래버스 (19년~현재)"
  ],
  "라세티": [
    "라세티 프리미어 (08년~11년)",
    "라세티 (02년~09년)"
  ],
  "카마로": [
    "더 뉴 카마로 (18년~22년)",
    "올 뉴 카마로 (16년~18년)",
    "카마로 (11년~15년)"
  ],
  "볼트EUV": [
    "볼트 EUV (21년~23년)"
  ],
  "타호": [
    "타호 (22년~현재)"
  ],
  "토스카": [
    "토스카 프리미엄6 (08년~11년)",
    "토스카 (06년~08년)"
  ],
  "볼트": [
    "볼트(Volt) (16년~19년)"
  ],
  "윈스톰": [
    "윈스톰 맥스 (08년~10년)",
    "윈스톰 (06년~10년)"
  ],
  "티코": [
    "티코 (91년~01년)"
  ],
  "QM6": [
    "더 뉴 QM6 (19년~현재)",
    "QM6 (16년~19년)"
  ],
  "SM6": [
    "더 뉴 SM6 (20년~현재)",
    "SM6 (16년~20년)"
  ],
  "SM5": [
    "SM5 노바 (15년~19년)",
    "뉴SM5 플래티넘 (12년~15년)",
    "뉴SM5(신형) (10년~12년)",
    "SM5 뉴 임프레션 (07년~10년)",
    "뉴SM5 (05년~07년)",
    "SM5 (98년~05년)"
  ],
  "SM3": [
    "SM3 네오 (14년~19년)",
    "SM3 Z.E. (13년~20년)",
    "뉴SM3 (09년~14년)",
    "SM3 뉴 제너레이션 (05년~11년)",
    "SM3 (02년~05년)"
  ],
  "XM3": [
    "XM3 (20년~24년)"
  ],
  "SM7": [
    "SM7 노바 (14년~19년)",
    "All New SM7 (11년~14년)",
    "SM7 New Art (08년~11년)",
    "SM7 (04년~08년)"
  ],
  "QM3": [
    "뉴QM3 (17년~19년)",
    "QM3 (13년~17년)"
  ],
  "QM5": [
    "QM5 네오 (14년~16년)",
    "뉴QM5 (11년~14년)",
    "QM5 (07년~11년)"
  ],
  "마스터": [
    "마스터 (18년~현재)"
  ],
  "조에": [
    "조에 (20년~22년)"
  ],
  "클리오": [
    "클리오 (18년~19년)"
  ],
  "캡처": [
    "캡처 (20년~21년)"
  ],
  "트위지": [
    "트위지 (17년~22년)"
  ],
  "아르카나": [
    "아르카나 (24년~현재)"
  ],
  "티볼리": [
    "더 뉴 티볼리 (23년~현재)",
    "더 뉴 티볼리 에어 (23년~현재)",
    "베리 뉴 티볼리 (19년~23년)",
    "티볼리 아머 (17년~19년)",
    "티볼리 에어 (16년~23년)",
    "티볼리 (15년~17년)"
  ],
  "렉스턴": [
    "렉스턴 뉴 아레나 (23년~현재)",
    "더 뉴 렉스턴 스포츠 (21년~현재)",
    "더 뉴 렉스턴 스포츠 칸 (21년~현재)",
    "올 뉴 렉스턴 (20년~23년)",
    "렉스턴 스포츠 칸 (19년~21년)",
    "렉스턴 스포츠 (18년~21년)",
    "G4 렉스턴 (17년~20년)",
    "렉스턴 W (12년~17년)",
    "슈퍼 렉스턴 (08년~12년)",
    "렉스턴 II (06년~08년)",
    "뉴렉스턴 (03년~06년)",
    "렉스턴 (01년~03년)"
  ],
  "코란도": [
    "코란도 EV (이모션) (22년~현재)",
    "뷰티풀 코란도 (19년~현재)",
    "뉴 스타일 코란도 C (17년~18년)",
    "더 뉴 코란도 스포츠 (16년~18년)",
    "뉴코란도 C (13년~17년)",
    "코란도 투리스모 (13년~19년)",
    "코란도 스포츠 (12년~16년)",
    "코란도 C (11년~13년)",
    "뉴코란도 (96년~05년)",
    "코란도 훼미리 (88년~96년)",
    "코란도 지프 (69년~96년)"
  ],
  "토레스": [
    "더 뉴 토레스 (24년~현재)",
    "토레스 EVX (23년~현재)",
    "토레스 (22년~24년)"
  ],
  "체어맨": [
    "뉴체어맨 W (11년~17년)",
    "체어맨 H 뉴 클래식 (11년~14년)",
    "체어맨 W (08년~11년)",
    "체어맨 H (08년~11년)",
    "뉴체어맨 (03년~08년)",
    "체어맨 (97년~03년)"
  ],
  "엑티언": [
    "액티언 스포츠 (06년~11년)",
    "액티언 (05년~11년)"
  ],
  "무쏘": [
    "무쏘 스포츠 (02년~06년)",
    "뉴무쏘 (98년~04년)",
    "뉴무쏘 밴 (98년~04년)",
    "무쏘 (93년~98년)"
  ],
  "카이런": [
    "뉴카이런 (07년~11년)",
    "카이런 (05년~07년)"
  ],
  "로디우스": [
    "로디우스 유로 (12년~13년)",
    "뉴로디우스 (07년~12년)",
    "로디우스 (04년~07년)"
  ],
  "이스타나": [
    "이스타나 (95년~03년)"
  ],
  "뉴훼미리": [
    "뉴훼미리 (94년~97년)"
  ],
  "칼리스타": [
    "칼리스타 (92년~94년)"
  ],
})
const openManufacturer = ref(null);
const openModel = ref(null);
const openDetailModel = ref(null);
// 제조사 및 모델 선택 상태 관리
const selectedManufacturer = ref(null);
const selectedModel = ref(null);
const selectedDetailModel = ref(null);

// 연식 상태 관리
const startYear = ref(null);
const endYear = ref(null);

// 최소 및 최대 주행거리 상태 관리
const minDistance = ref(null);
const maxDistance = ref(null);

// 디스플레이용 주행거리 변수
const minDistanceDisplay = ref(null);
const maxDistanceDisplay = ref(null);

// 최소 및 최대 가격 상태 관리
const minPrice = ref(null);
const maxPrice = ref(null);

// 가격 옵션 생성
const priceOptions = [];

// 제조사 이름 맵핑
const manufacturerMapping = {
  "쉐보레(GM대우)": "쉐보레",
  "르노코리아(삼성)": "르노코리아",
  "KG모빌리티(쌍용)": "쌍용",
};

// 최근 검색조건 상태 관리 -> 제조사, 모델
const recentSearchCondition = ref(JSON.parse(sessionStorage.getItem('recentSearchCondition')) || []);

// 최근 검색조건에 추가하는 함수
const addRecentSearchCondition = () => {
  if (selectedManufacturer.value && selectedModel.value) {
    // 중복된 검색 조건인지 확인
    const existingCondition = recentSearchCondition.value.find(
      (condition) => condition.manufacturer === selectedManufacturer.value && condition.model === selectedModel.value
    );

    if (!existingCondition) {
      // 최근 검색 조건이 5개를 초과하면 가장 오래된 조건을 제거
      if (recentSearchCondition.value.length >= 5) {
        recentSearchCondition.value.shift(); // 가장 오래된 조건 제거
      }

      // 새로운 검색 조건 추가
      recentSearchCondition.value.push({
        manufacturer: selectedManufacturer.value,
        model: selectedModel.value,
      });
      sessionStorage.setItem('recentSearchCondition', JSON.stringify(recentSearchCondition.value));
    }
  }
};


// 0만원부터 2000만원까지 100만원 단위로 추가
for (let i = 100; i <= 2000; i += 100) {
  priceOptions.push(`${i}만원`);
}

// 2000만원부터 10000만원까지 1000만원 단위로 추가
for (let i = 3000; i <= 10000; i += 1000) {
  priceOptions.push(`${i}만원`);
}


// 주행거리 옵션 배열 생성
const distanceOptions = Array.from({ length: 20 }, (_, i) => `${(i + 1) * 10000} km`);

// 주행거리 옵션 배열 생성 (콤마 추가된 옵션)
const formattedDistanceOptions = distanceOptions.map((distance) => {
  return new Intl.NumberFormat().format(parseInt(distance)) + ' km';
});



// 연도 및 월 옵션
const yearOptions = [];
for (let year = 1980; year <= 2024; year++) {
  yearOptions.push(year.toString());
}

// 연도 옵션 배열 생성
const filteredYearOptions = computed(() => {
  if (startYear.value) {
    return yearOptions.filter(year => parseInt(year) >= parseInt(startYear.value));
  }
  return yearOptions;
});


// 드롭다운 토글
const toggleCarTypeDropdown = () => {
  isCarTypeDropdownOpen.value = !isCarTypeDropdownOpen.value;
};
const toggleYearDropdown = () => {
  isYearDropdownOpen.value = !isYearDropdownOpen.value;
};
const toggleDistanceDropdown = () => {
  isDistanceDropdownOpen.value = !isDistanceDropdownOpen.value;
};
const togglePriceDropdown = () => {
  isPriceDropdownOpen.value = !isPriceDropdownOpen.value;
};
const toggleRecentSearch = () => {
  isRecentSearchOpen.value = !isRecentSearchOpen.value;
};

  // 제조사 클릭 시 해당 제조사에 대한 모델 목록 표시
  const toggleManufacturer = (manufacturer) => {
    if (openManufacturer.value === manufacturer) {
      openManufacturer.value = null; // 제조사 클릭 시 닫기
    } else {
      openManufacturer.value = manufacturer; // 선택한 제조사 열기
      selectedManufacturer.value = manufacturer; // 선택한 제조사 저장
      sessionStorage.setItem('selectedManufacturer', JSON.stringify(selectedManufacturer.value));
      const apiManufacturer = manufacturerMapping[manufacturer] || manufacturer; // API에 전달할 제조사 이름 결정
      search.value.manufacturers = apiManufacturer; // API 호출을 위해 선택된 제조사 저장
      GetProductList(); // API 호출

    }
  };

// 모델 클릭시 해당 모델 선택 및 세부 모델 표시
const toggleModel = (model) => {
  if (openModel.value === model) {
    openModel.value = null; // 모델 클릭 시 닫기
  } else {
    openModel.value = model; // 선택한 모델 열기
    selectedModel.value = model; // 선택한 모델 저장
    sessionStorage.setItem('selectedModel', JSON.stringify(selectedModel.value));
    search.value.name = model; // API 호출을 위해 선택된 모델 저장
    openDetailModel.value = null; // 세부 모델 목록 초기화
  }
  if (selectedModel.value) {
        addRecentSearchCondition();
      }
  GetProductList(); // API 호출
};

// 세부 모델 클릭 시 해당 세부 모델 선택
const toggleDetailModel = (model) => {
  if (openDetailModel.value === model) {
    openDetailModel.value = null; // 세부 모델 클릭 시 닫기
  } else {
    openDetailModel.value = model; // 선택한 세부 모델 열기
    selectedDetailModel.value = model; // 선택한 세부 모델 저장
    sessionStorage.setItem('selectedDetailModel', JSON.stringify(selectedDetailModel.value));
    search.value.grade = model; // API 호출을 위해 선택된 세부 모델 저장
    console.log("세부모델 선택:", model);
  }
  GetProductList(); // API 호출
};


// 선택된 제조사 초기화
const clearSelectedManufacturer = () => {
  selectedManufacturer.value = null;
  openManufacturer.value = null;
  search.value.manufacturers = "";
  GetProductList(); // API 호출
};

  // 선택된 모델 초기화
  const clearSelectedModel = () => {
    selectedModel.value = null;
    openModel.value = null; // 모델 열림 상태 초기화
    search.value.name = "";
    GetProductList(); // API 호출
  };

// 선택된 세부모델 초기화
const clearSelectedDetailModel = () => {
  selectedDetailModel.value = null;
  search.value.grade = "";
  GetProductList(); // API 호출
};


const filteredManufacturers = computed(() => {
  if (selectedManufacturer.value) {
    return [selectedManufacturer.value]; // 선택된 제조사만 반환
  }
  return manufacturers; // 선택된 제조사가 없으면 전체 제조사 반환
});

const filteredModels = computed(() => {
  if (selectedModel.value) {
    return [selectedModel.value]; // 선택된 모델만 반환
  }
  return modelsByManufacturer.value[selectedManufacturer.value] || []; // 선택된 제조사의 모델 목록 반환
});


// 결과값 변수 설정
const result = ref({ products: [], total: 0 });
const search = ref({
  page: 1,
  limit: 12,
  manufacturers: "",
  types: "",
  min_price: "",
  max_price: "",
  min_distance: "",
  max_distance: "",
  min_year: "",
  max_year: "",
  name:"",
  grade: "",
 });

// 현재 페이지 및 최대 페이지 설정
const currentPage = ref(search.value.page);
const maxPages = computed(() => Math.ceil(result.value.total / search.value.limit));

const NoResult = ref(false)

// API 호출
const GetProductList = async () => {

  $q.loading.show({
    message: '로딩중입니다.', // 표시할 메시지
    spinnerSize: 40,       // 스피너 크기 (원하는 경우 설정)
  });
  if (search.value.max_distance === 0) {
    search.value.max_distance = null;
  }
  if (search.value.min_distance === 0) {
    search.value.min_distance = null;
  }

  const url = `${process.env.API}products?page=${search.value.page}&limit=${search.value.limit}&manufacturers=${search.value.manufacturers}&types=${search.value.types}&name=${search.value.name}&min_year=${search.value.min_year}&max_year=${search.value.max_year}&min_distance=${search.value.min_distance}&max_distance=${search.value.max_distance}&min_price=${search.value.min_price}&max_price=${search.value.max_price}&grade=${search.value.grade}&category=domestic`;

  try {
    const res = await api.get(url);
    if (res.data.total === 0) {
      NoResult.value = true;
    } else {
      NoResult.value = false;
    }
    result.value = res.data;
    console.log("API 호출 결과 확인", result.value);
    // search.value.totalPages = Math.ceil(result.value.total / search.value.limit);
  } catch (err) {
    console.log(err);
  } finally {
    // 로딩 종료
    $q.loading.hide();
  }
};

const domesticProductCount = ref(0);
const GetDomesticProductCount = () => {

  const url = `${process.env.API}count_products?category=domestic`;

  api.get(url)
    .then((res) => {
      console.log("국산차 수량 확인", res.data);
      domesticProductCount.value = res.data.count;
    })
    .catch((err) => {
      console.log(err);
    });
};
// 관심상품 목록
const interestProducts = ref([]);

// 관심상품 목록 API 호출
const GetUserInterestProduct = () => {
  const url = `${process.env.API}user/interest_products`;

  api.get(url, {
    withCredentials: true  // 쿠키를 포함하여 요청
  })
    .then((res) => {
      console.log("관심상품 목록 확인", res.data);
      interestProducts.value = res.data;
    })
    .catch((err) => {
      console.log(err);
    });
};

// 상품이 관심상품인지 확인하는 함수
const isInterestProduct = (productId) => {
  console.log("관심상품 목록 확인", interestProducts.value);
  return interestProducts.value.some(item => item.product_id === productId);
};




const goDetail = (detailId) => {
  console.log("detailId", detailId);
  $router.push({
    path: `/product/ProductDetail/${detailId}`,
  });
};

const changePage = async (page) => {
  if (page !== search.value.page) {  // 중복 호출 방지를 위해 동일한 페이지로 이동 시 호출하지 않음
    search.value.page = page;  // search.page만 업데이트
    await GetProductList();  // 한 번만 API 호출
  }
};

// 가격을 숫자로 변환하는 함수 (만원 단위를 원으로 변환한 후 문자열로 처리)
const parsePriceToString = (price) => {
  return price ? (parseInt(price.replace('만원', '')) * 10000).toString() : "";
};
// 검색조건 저장
const saveSearchConditions = () => {
  sessionStorage.setItem('searchConditions', JSON.stringify(search.value));
  sessionStorage.setItem('selectedCarTypes', JSON.stringify(selectedCarTypes.value));
  sessionStorage.setItem('selectedManufacturer', JSON.stringify(selectedManufacturer.value));
  sessionStorage.setItem('selectedModel', JSON.stringify(selectedModel.value));
  sessionStorage.setItem('startYear', JSON.stringify(startYear.value));
  sessionStorage.setItem('endYear', JSON.stringify(endYear.value));
};

// 최근 검색조건 초기화
const clearRecentSearches = () => {
  recentSearchCondition.value = [];
  sessionStorage.removeItem('recentSearchCondition');
};

// 페이지 로드 시 검색 조건 복원
// const loadSearchConditions = () => {
//   const savedConditions = sessionStorage.getItem('searchConditions');
//   if (savedConditions) {
//     search.value = JSON.parse(savedConditions);
//   }
//   const savedCarTypes = sessionStorage.getItem('selectedCarTypes');
//   if (savedCarTypes) {
//     selectedCarTypes.value = JSON.parse(savedCarTypes);
//   }
//   const savedManufacturer = sessionStorage.getItem('selectedManufacturer');
//   if (savedManufacturer) {
//     selectedManufacturer.value = JSON.parse(savedManufacturer);
//   }
//   const savedModel = sessionStorage.getItem('selectedModel');
//   if (savedModel) {
//     selectedModel.value = JSON.parse(savedModel);
//   }
// };

const createInterestProduct = (id) => {
  const url = `${process.env.API}create/interest_product`;

  api.post(url, { product_id: id },{
  withCredentials: true  // 쿠키를 포함하여 요청
  })
  .then((res) => {
      console.log("관심상품 등록 결과 확인", res.data);
        $q.notify({
          color: 'positive',
          position: 'top',
          message: '관심상품으로 등록되었습니다.',
          icon: 'check',
        });
    })
  .catch((err) => {
      console.log(err);
    });
};


const resetAll = () => {
  search.value = {
    page: 1,
    limit: 12,
    manufacturers: "",
    types: "",
    min_price: "",
    max_price: "",
    min_distance: "",
    max_distance: "",
    min_year: "",
    max_year: "",
    name:"",
    grade: "",
  };
  selectedCarTypes.value = [];
  selectedManufacturer.value = null;
  selectedModel.value = null;
  selectedDetailModel.value = null;
  startYear.value = null;
  endYear.value = null;
  minDistance.value = null;
  maxDistance.value = null;
  minPrice.value = null;
  maxPrice.value = null;
  minDistanceDisplay.value = null;
  maxDistanceDisplay.value = null;

  GetProductList();
};


// const parseDistance = (distance) => {
//   // distance가 문자열인 경우에만 km 제거
//   return typeof distance === 'string' ? distance.replace(' km', '') : null;
// };

// watch example
watch(selectedManufacturer, (newVal, oldVal) => {
  console.log("선택된 제조사가 변경되었습니다:", newVal);
  if (newVal) {
    // 선택된 제조사에 대한 추가 작업 실행 가능
  }
});

// 검색 조건 변경 시 저장
watch(search, (newVal, oldVal) => {
  if (isInitialLoad) {
    isInitialLoad = false;
  } else if (newVal.page !== oldVal.page) {
    saveSearchConditions();
    GetProductList();
  } else {
    saveSearchConditions();
  }
}, { deep: true });

// 차종 변경 시 API 호출
watch(selectedCarTypes, (newVal) => {

  // 소형차 -> 소형 변환
  if (newVal.includes("소형차")) {
    newVal = newVal.filter((type) => type !== "소형차");
    newVal.push("소형");
  }
  if (newVal.includes("준중형차")) {
    newVal = newVal.filter((type) => type !== "준중형차");
    newVal.push("준중형");
  }
  if (newVal.includes("중형차")) {
    newVal = newVal.filter((type) => type !== "중형차");
    newVal.push("중형");
  }
  if (newVal.includes("대형차")) {
    newVal = newVal.filter((type) => type !== "대형차");
    newVal.push("대형");
  }
  if (newVal.includes("스포츠카")) {
    newVal = newVal.filter((type) => type !== "스포츠카");
    newVal.push("스포츠");
  }
  if (newVal.includes("SUV")) {
    newVal = newVal.filter((type) => type !== "SUV");
    newVal.push("SUV");
  }
  if (newVal.includes("RV")) {
    newVal = newVal.filter((type) => type !== "RV");
    newVal.push("RV");
  }

  search.value.types = newVal.join(','); // 배열을 ,로 연결한 문자열로 변환하여 search.value.types에 저장
  console.log("선택된 차종:", search.value.types);
  // API 호출 업데이트
  GetProductList();
});

// 최소 및 최대 가격 상태가 변경될 때마다 API 호출
watch([minPrice, maxPrice], ([newMinPrice, newMaxPrice]) => {
  search.value.min_price = parsePriceToString(newMinPrice); // 숫자를 문자열로 변환해서 저장
  search.value.max_price = parsePriceToString(newMaxPrice);
  console.log("가격 변경:", search.value.min_price, search.value.max_price);
  GetProductList();
});


// 연식 변경 시 API 호출
watch([startYear, endYear], ([newStartYear, newEndYear]) => {
  search.value.min_year = newStartYear || "";
  search.value.max_year = newEndYear || "";
  GetProductList(); // 연식 변경 시 API 호출
});

watch(minDistanceDisplay, (newVal) => {
  // 콤마를 제거하고 숫자만 추출하여 실제 minDistance에 저장
  minDistance.value = newVal ? newVal.replace(/,/g, '').replace(' km', '') : null;
});

watch(maxDistanceDisplay, (newVal) => {
  // 콤마를 제거하고 숫자만 추출하여 실제 maxDistance에 저장
  maxDistance.value = newVal ? newVal.replace(/,/g, '').replace(' km', '') : null;
});


// 주행거리 상태 변경 시
watch([minDistance, maxDistance], ([newMinDistance, newMaxDistance]) => {
  search.value.min_distance = newMinDistance || "";
  search.value.max_distance = newMaxDistance || "";

  GetProductList(); // API 호출
});


onMounted(() => {
  const { manufacturer, model, subModel } = route.query;

  if (manufacturer) {
    selectedManufacturer.value = manufacturer;
    search.value.manufacturers = manufacturer;
  }

  if (model) {
    selectedModel.value = model;
    search.value.name = model;
  }

  if (subModel) {
    selectedDetailModel.value = subModel;
    search.value.grade = subModel;
  }

  // 페이지 로드 시 초기 검색 조건에 따른 결과 리스트 호출
  GetProductList();
  GetDomesticProductCount();
  GetUserInterestProduct();
});

</script>

<style scoped>
.main-container {
  display: flex;
}

.search-bar {
  /* height: 1000px; */
  width: 270px;
  /* border: 1px solid #000; */
}

.item-area {
  width: 100%; /* 상품 리스트 영역이 컨테이너의 전체 너비를 차지하도록 설정 */
  display: flex;
  flex-wrap: wrap; /* 아이템들이 자동으로 줄 바꿈되도록 설정 */
  gap: 16px; /* 아이템 간의 간격 설정 */
  /* border: 1px solid red; */
}

.pro-box {
  width: calc(25% - 16px); /* 1줄에 4개의 아이템을 표시하기 위해 너비를 설정, gap을 제외 */
  box-sizing: border-box; /* padding과 border를 포함한 너비 계산 */
  border: 1px solid #ddd; /* 아이템의 테두리 설정 */
  padding: 8px;
  background-color: #fff;
  border-radius: 6px;
  cursor: pointer;
  height: 345px;
}
.pro-img {
  width: 100%; /* 부모 박스의 너비에 맞도록 설정 */
  height: auto; /* 높이는 비율에 맞게 자동 조정 */
  background: #f5f5f5; /* 기본 배경색 설정 */
  display: flex;
  align-items: center;
  justify-content: center;
  object-fit: cover;
}
.pro-img img {
  width: 100%; /* 이미지가 박스의 전체 너비를 차지하도록 설정 */
  height: auto; /* 높이를 자동으로 조정하여 이미지 비율을 유지 */
  object-fit: cover; /* 이미지가 박스 영역에 꽉 차게 설정 */
}

.pro-info {
  padding: 8px 0;
}

.se-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 10px;
  padding-top: 10px;
}

.se-middle {
  display: flex;
  gap: 20px;
  padding: 10px;
}

.filter-section {
  /* margin-top: 20px; */
  border: 1px solid #ddd;
  padding: 10px;
}

.dropdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  padding: 5px 10px;
  background-color: #f5f5f5;
  border-radius: 5px;
}

.dropdown-body {
  /* padding: 10px; */
  display: flex;
  flex-direction: column;
  /* gap: 10px; */
  background-color: #fafafa;
  margin-top: 10px;
  border-radius: 10px;
  padding-left: 10px;
}
.selected-manufacturer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px;
  /* background-color: #e0e0e0; */
  border-radius: 5px;
  font-weight: bold;
  color: #f73434;
}

.manufacturer-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.manufacturer-item {
  cursor: pointer;
  padding: 5px 10px;
  background-color: #f9f9f9;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.manufacturer-item:hover {
  /* background-color: #dcdcdc; */
}

.model-list {
  margin-top: 10px;
  max-height: 200px; /* 고정된 높이 설정 */
  overflow-y: auto; /* 세로 스크롤 추가 */
  /* padding: 10px; */
  background-color: #fafafa;
}

.model-item {
  padding: 5px;
  background-color: #f1f1f1;
  border-radius: 5px;
  margin-bottom: 5px;
}

.pro-title {
  font-weight: bold;
  word-break: keep-all;
}

.pro-details {
  display: flex;
  align-items: center;
  color: #757575
  /* gap: 8px; 아이템 간의 간격 설정 */
}
.pro-details-2 {
  display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-top: 10px;
}

.pro-separator {
  margin: 0 8px; /* 양쪽 여백 설정 */
}
.pro-price{
  font-weight: bold;
}
.price-text{
 font-size: 16px;
 padding-right: 3px;
}
.page-box{
  width: 100%;
  /* justify-content: center; */
}
.custom-pagination{
  display: flex;
  justify-content: center;
}
.custom-pagination .q-pagination__page {
  margin: 0 4px;
}

.custom-pagination .q-pagination__page--active {
  background-color: #027be3;
  color: white;
}
.se-title {
    font-size: 18px;
    color: #ff3333;
    font-weight: 700;
}
.se-quan {
    font-size: 14px;
    font-weight: bold;
    letter-spacing: -0.5px;
    color: #555;
}
.pro-sub1{
  font-size: 12px;
    border: 1.5px solid #f18f4e;
    border-radius: 3px;
    padding: 4px;
    color: #f18f4e;
    font-family: Pretendard;
}
.pro-sub2{
  font-size: 13px;
  padding: 4px;
    border: 1.5px solid #4367d6;
    border-radius: 3px;
    color: #4367d6;
    margin-top: 5px;
    font-family: Pretendard;
}
.distance-selection {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
.price-selection {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
.reset-btn{
  cursor: pointer;
}
.recent-search {
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  padding: 10px;
  margin-top: 10px;
}
.recent-search-items{
  display: flex ;
  flex-direction: column;
}
.recent-cont{
  font-weight: bold;
    padding: 5px;
    display: flex;
    justify-content: space-between;
}
/* 체크박스와 라벨의 위치를 조정하는 CSS */
.checkbox-container {
  display: flex;
  align-items: center; /* 체크박스와 라벨을 수직 중앙 정렬 */
  margin-bottom: 8px; /* 항목 간 간격 */
}

.checkbox-label {
  display: flex;
  align-items: center;
  /* 체크박스와 라벨 사이의 간격 조정 */
  gap: 10px;
}

.custom-checkbox {
  appearance: none; /* 브라우저 기본 스타일 제거 */
  width: 16px;
  height: 16px;
  border: 2px solid #ccc; /* 외곽선 색상을 옅은 회색으로 설정 */
  border-radius: 3px;
  vertical-align: middle; /* 체크박스를 텍스트 높이에 맞춤 */
  background-color: #f5f5f5; /* 체크박스 배경 색상 */
}
.custom-checkbox:checked {
  background-color: #ccc; /* 체크된 상태의 배경 색상 */
  border-color: #888; /* 체크된 상태의 외곽선 색상 */
}

.custom-checkbox:checked::before {
  content: "\2713"; /* 체크 표시 */
  color: white;
  font-size: 12px;
  display: block;
  text-align: center;
  line-height: 16px; /* 체크 표시를 중앙에 정렬 */
}

.no-result {
    margin: 0 auto;
    font-weight: bold;
    padding-top: 30px;
}
.recent-search-btn{
  cursor: pointer;
}
.pro-mileage{
  font-size: 12px;
}
.pro-year{
  font-size: 12px;
}
.del-btn{
  border: none;
  /* background-color: #e0e0e0; */
  color: #757575;
}
.q-select--without-input .q-field__control {
    cursor: pointer;
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    /* font-size: 20px; */
    height: 35px;
    border-radius: 5px;
}
.year-selection {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.bookmark-btn {
  position: absolute;
    /* bottom: 13px; */
    /* right: 10px; */
    background-color: rgba(0, 0, 0, 0.5);
    color: white;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    cursor: pointer;
    opacity: 0;
    /* transition: all 0.4s ease; */
    /* margin-top: 41px; */
    transform: translate(0px, 10px);
    width: 100%;
}

.pro-img-wrapper:hover .bookmark-btn {
  bottom: 10px; /* Move the button up to its final position */
  opacity: 1; /* Make the button visible */
}

.pro-img-wrapper {
  position: relative;
  width: 100%;
  height: auto;
}
.interest-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: red;
  color: white;
  padding: 5px;
  border-radius: 5px;
  font-size: 12px;
  font-weight: bold;
}

</style>
