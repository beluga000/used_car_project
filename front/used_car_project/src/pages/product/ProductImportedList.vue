<template>
  <q-layout class="page-container page-background">
    <q-page class="common-container-1">
      <div class="main-container">
        <!-- 검색창 영역 -->
        <div class="search-bar">
          <div class="se-top">
            <div class="se-title">
              수입차 검색
            </div>
            <div class="se-quan">
              {{importedProductCount}}대
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
              <div class="recent-cont" v-for="(condition, index) in recentSearchImportedCondition" :key="index">
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
              @click.stop="createNrefresh(product.id)"
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
  name: "ProductImportedList",
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
const manufacturers =  ['BMW', '벤츠', '볼보', '아우디', '테슬라', '포르쉐','랜드로버','닛산','링컨','포드','폭스바겐','미니','캐딜락','토요타','렉서스','애스턴마틴','마세라티','푸조','지프','혼다','재규어','인피니티','폴스타'];
const modelsByManufacturer = ref({
  "BMW":["5시리즈","3시리즈","7시리즈","그란투리스모(GT)","X6","X5","4시리즈","X3","1시리즈","X7","X4","2시리즈","Z4","X1","M4","M3","M2","iX3","i4","6시리즈","M5","8시리즈","X4M","i3","X2","iX","i8","X3M","X6M","X5M","i7","M6","i5","XM","M8","Z3","1M","iX1","M쿠페/로드스터","Z8","기타"],
  "벤츠":["E클래스","S클래스","C클래스","GLC클래스","CLS클래스","GLE클래스","A클래스","CLA클래스","G클래스(G바겐)","GLA클래스","AMG GT","GLB클래스","EQS","EQE","GLS클래스","EQB","EQA","SL클래스","M클래스","SLK클래스","B클래스(MY B)","스프린터","GLK클래스","CLE클래스","SLC클래스","V클래스","CL클래스","EQC","CLK클래스","SEL/SEC","GL클래스","SLS AMG","R클래스","190클래스","기타","SLR"],
  "볼보":["XC60","XC90","S90","S60","XC40","V60","V40","V90","S80","C40","XC70","C30","S40","S70","940","V50","C70","EX30","V70","740","760","850","960","기타"],
  "아우디":["A6","A7","A4","A8","Q5","A5","Q7","Q8","A3","R8","e-트론","Q3","Q4 e-트론","S7","S8","TT","RS7","S4","S6","SQ5","RS5","Q2","S3","TTS","RSQ8","e-트론 GT","S5","RS e-트론 GT","A1","RS3","SQ8","SQ7","100","80","90","RS4","RS6","TTRS","V8","Q8 e-트론","SQ8 e-트론","올로드 콰트로","기타"],
  "테슬라":["모델 3","모델 Y","모델 X","모델 S"],
  "포르쉐":["카이엔","파나메라","718","911","마칸","타이칸","박스터","카이맨","928","944","968","카레라 GT","기타"],
  "랜드로버":["레인지로버","디스커버리","디스커버리 스포츠","레인지로버 스포츠","레인지로버 이보크","레인지로버 벨라","디펜더","프리랜더","기타"],
  "닛산":["리프","알티마","리프","370Z","큐브","맥시마","쥬크","무라노","패스파인더","엑스트레일","로그","스카이라인","캐시카이","350Z","GT-R","마치","휘가로","프론티어","NV","노트","로렐","모코","버사","베르사","블루버드 실피","블루버드","세드릭"],
  "링컨":["MKZ","에비에이터","MKS","컨티넨탈","네비게이터","MKX","노틸러스","MKC","코세어","타운카","LS","MKT"],
  "포드":["포커스","익스플로러","머스탱","F150","토러스","몬데오","레인저","쿠가","퓨전","브롱코","이스케이프","F350","E-Series","트랜짓","F250","익스플로러 스포츠트랙","프리스타일","GT","S-MAX","썬더버드","윈드스타","이코노라인","에코스포츠","컨투어","파이브 헌드레드","프로브","피에스타","기타","플렉스"],
  "폭스바겐":["티구안","골프","아테온","제타","파사트","CC","투아렉","비틀","폴로","시로코","티록","페이톤","ID.4","EOS","보라","기타","리알타","마이크로버스","벤토","사란","아틀라스","코라도","트랜스포터"],
  "미니":["쿠퍼","컨트리맨","클럽맨","쿠퍼 컨버터블","쿠페","페이스맨","로드스터","로버 미니"],
  "캐딜락":["에스컬레이드","CT6","CTS","ATS","XT5"],
  "토요타":["캠리","프리우스","RAV4","시에나","86","알파드","크라운","FJ 크루져"],
  "렉서스":["ES","NX","RX","LS","UX","CT200h","IS","GS","RC","RZ","LC","SC","GX","LX","기타"],
  "애스턴마틴":["DB11","밴티지","DBX","라피드","DBS","DB9","뱅퀴시","DB7","비라지"],
  "마세라티":["기블리","르반떼","콰트로포르테","그란투리스모","그레칼레","MC20","그란카브리오","쿠페","스파이더","그란스포츠","3200","MC12","기타"],
  "푸조":["3008","2008","508","5008","208","308","207","RCZ","206","408","307","407","익스퍼트","107","1007","205","306","405","406","605","607","806","807","기타"],
  "지프":["랭글러","체로키","레니게이드","글래디에이터","컴패스","커맨더","CJ","패트리어트"],
  "혼다":["어코드","파일럿","CR-V","오딧세이","시빅","레전드","HR-V","CR-Z","S660","N-BOX","S2000","스텝웨건","인사이트","크로스투어","Fit Aria","Fit","N-ONE","댓츠","델솔","라이프","리지라인","비트","스트림","엘리멘트","인스파이어","인테그라","크로스로드","패스포트","프렐류드","기타"],
  "재규어":["XF","XJ","XE","F-PACE","F-TYPE","E-PACE","I-PACE","X-TYPE","XJ-8","S-TYPE","XJ-6","XKR","다임러","XJR","소버린","XJ-C","XK8","기타","XJS","XK"],
  "인피니티":["Q50","G","Q30","M","QX60","Q70","QX50","FX","Q60","QX80","QX30","EX","JX","QX","QX70","I","Q","J30"],
  "폴스타":["폴스타2"]
});
const detailModelsBymodels = ref({
  "5시리즈":[
    "5시리즈 (G60) (23년~현재)",
    "5시리즈 (G30) (17년~23년)",
    "5시리즈 (F10) (10년~16년)",
    "5시리즈 (E60) (03년~10년)",
    "5시리즈 (72년~03년)"
  ],
  "3시리즈":[
    "3시리즈 (G20) (19년~현재)",
    "3시리즈 (F30) (12년~18년)",
    "3시리즈 (E90) (05년~13년)",
    "3시리즈 (75년~06년)"
  ],
  "7시리즈":[
    "7시리즈 (G70) (22년~현재)",
    "7시리즈 (G11) (15년~22년)",
    "7시리즈 (F01) (08년~15년)",
    "7시리즈 (E65) (02년~08년)",
    "7시리즈 (77년~01년)"
  ],
  "그란투리스모(GT)":[
    "6시리즈 GT (G32) (17년~현재)",
    "3시리즈 GT (F34) (13년~현재)",
    "5시리즈 GT (F07) (10년~17년)"
  ],
  X6:[
    "X6 (G06) (19년~현재)",
    "X6 (F16) (14년~19년)",
    "X6 (E71) (08년~14년)"
  ],
  X5:[
    "X5 (G05) (19년~현재)",
    "X5 (F15) (13년~18년)",
    "X5 (E70) (07년~13년)",
    "X5 (E53) (00년~06년)"
  ],
  "4시리즈":[
    "4시리즈 (G22) (21년~현재)",
    "4시리즈 (F32) (13년~20년)"
  ],
  X3:[
    "X3 (G01) (17년~현재)",
    "X3 (F25) (11년~17년)",
    "X3 (E83) (04년~10년)"
  ],
  "1시리즈":[
    "1시리즈 (F40) (20년~현재)",
    "1시리즈 (F20) (12년~19년)",
    "1시리즈 (E82) (04년~13년)"
  ],
  X7:[
    "X7 (G07) (19년~현재)"
  ],
  X4:[
    "X4 (G02) (18년~현재)",
    "X4 (F26) (14년~18년)"
  ],
  "2시리즈":[
    "2시리즈 액티브 투어러 (U06) (22년~현재)",
    "2시리즈 (G42) (22년~현재)",
    "2시리즈 그란쿠페 (F44) (20년~현재)",
    "2시리즈 액티브 투어러 (F45) (15년~22년)",
    "2시리즈 (F22) (13년~15년)"
  ],
  Z4:[
    "Z4 (G29) (19년~현재)",
    "Z4 (E89) (09년~16년)",
    "Z4 (E85) (02년~08년)"
  ],
  X1:[
    "X1 (U11) (23년~현재)",
    "X1 (F48) (16년~23년)",
    "X1 (E84) (10년~15년)"
  ],
  M4:[
    "M4 (G82) (21년~현재)",
    "M4 (F82) (14년~21년)"
  ],
  M3:[
    "M3 (G80) (21년~현재)",
    "M3 (F80) (14년~21년)",
    "M3 (E90) (07년~13년)",
    "M3 (E46) (00년~06년)",
    "M3 (E36) (92년~99년)"
  ],
  iX3: [
    "iX3 (21년~현재)"
  ],
  M2: [
    "M2 (G87) (23년~현재)",
    "M2 (F87) (16년~23년)"
  ],
  i4: [
    "i4 (21년~현재)"
  ],
  "6시리즈": [
    "6시리즈 (F12) (11년~18년)",
    "6시리즈 (E63) (03년~10년)"
  ],
  M5: [
    "M5 (F90) (18년~현재)",
    "M5 (F10) (12년~17년)",
    "M5 (E60) (05년~10년)",
    "M5 (E39) (98년~03년)",
    "M5 (E34) (88년~95년)",
    "M5 (E28) (84년~88년)"
  ],
  "8시리즈": [
    "8시리즈 (G15) (19년~현재)",
    "8시리즈 (89년~99년)"
  ],
  X4M: [
    "X4M (G02) (19년~현재)"
  ],
  i3: [
    "i3 (14년~현재)"
  ],
  X2: [
    "X2 (U10) (24년~현재)",
    "X2 (F39) (18년~24년)"
  ],
  iX: [
    "iX (21년~현재)"
  ],
  X3M: [
    "X3M (G01) (19년~현재)"
  ],
  i8: [
    "i8 (14년~현재)"
  ],
  X6M: [
    "X6M (G06) (20년~현재)",
    "X6M (F16) (15년~19년)",
    "X6M (E71) (09년~14년)"
  ],
  X5M: [
    "X5M (G05) (20년~현재)",
    "X5M (F15) (15년~18년)",
    "X5M (E70) (10년~13년)"
  ],
  i7: [
    "i7 (G70) (22년~현재)"
  ],
  M6: [
    "M6 (F12) (12년~18년)",
    "M6 (E63) (05년~10년)"
  ],
  i5: [
    "i5 (G60) (23년~현재)"
  ],
  XM: [
    "XM (G09) (23년~현재)"
  ],
  M8: [
    "M8 (G15) (19년~현재)"
  ],
  "1M": [
    "1M (E82) (11년~12년)"
  ],
  Z3: [
    "Z3 (96년~02년)"
  ],
  iX1: [
    "iX1 (U11) (23년~현재)"
  ],
  M쿠페_로드스터: [
    "M 쿠페/로드스터 (E85) (06년~08년)",
    "M 쿠페/로드스터 (E36) (98년~02년)"
  ],
  Z8: [
    "Z8 (99년~03년)"
  ],
  E클래스: [
    "E-클래스 W214 (24년~현재)",
    "E-클래스 W213 (16년~현재)",
    "E-클래스 W212 (09년~17년)",
    "E-클래스 W211 (02년~09년)",
    "E-클래스 W210 (95년~02년)",
    "E-클래스 W124 (84년~95년)",
    "E-클래스 W123 (76년~85년)"
  ],
  S클래스: [
    "S-클래스 W223 (21년~현재)",
    "S-클래스 W222 (13년~21년)",
    "S-클래스 W221 (05년~13년)",
    "S-클래스 (93년~06년)"
  ],
  C클래스: [
    "C-클래스 W206 (22년~현재)",
    "C-클래스 W205 (14년~현재)",
    "C-클래스 W204 (07년~14년)",
    "C-클래스 (93년~07년)"
  ],
  GLC클래스: [
    "GLC-클래스 X254 (23년~현재)",
    "GLC-클래스 X253 (16년~23년)"
  ],
  CLS클래스: [
    "CLS-클래스 C257 (18년~현재)",
    "CLS-클래스 W218 (11년~17년)",
    "CLS-클래스 W219 (04년~11년)"
  ],
  GLE클래스: [
    "GLE-클래스 W167 (19년~현재)",
    "GLE-클래스 W166 (16년~19년)"
  ],
  A클래스: [
    "A-클래스 W177 (19년~현재)",
    "A-클래스 W176 (13년~18년)",
    "A-클래스 W169 (04년~12년)",
    "A-클래스 W168 (97년~04년)"
  ],
  CLA클래스: [
    "CLA-클래스 C118 (20년~현재)",
    "CLA-클래스 C117 (14년~19년)"
  ],
  G클래스: [
    "G-클래스 W463b (19년~현재)",
    "G-클래스 W463 (79년~18년)"
  ],
  GLA클래스: [
    "GLA-클래스 H247 (20년~현재)",
    "GLA-클래스 X156 (14년~20년)"
  ],
  AMG_GT: [
    "AMG GT (14년~현재)"
  ],
  GLB클래스: [
    "GLB-클래스 X247 (20년~현재)"
  ],
  EQS: [
    "EQS SUV X296 (23년~현재)",
    "EQS V297 (21년~현재)"
  ],
  EQE: [
    "EQE SUV X294 (23년~현재)",
    "EQE V295 (22년~현재)"
  ],
  GLS클래스: [
    "GLS-클래스 X167 (20년~현재)",
    "GLS-클래스 X166 (16년~19년)"
  ],
  EQB: [
    "EQB X243 (22년~현재)"
  ],
  EQA: [
    "EQA H243 (21년~현재)"
  ],
  SL클래스: [
    "SL-클래스 R232 (23년~현재)",
    "뉴 SL-클래스 (08년~20년)",
    "SL-클래스 (54년~08년)"
  ],
  M클래스: [
    "M-클래스 W166 (12년~15년)",
    "M-클래스 W164 (05년~11년)",
    "M-클래스 W163 (97년~05년)"
  ],
  SLK클래스: [
    "뉴 SLK-클래스 (04년~16년)",
    "SLK-클래스 (96년~04년)"
  ],
  B클래스: [
    "B-클래스 W246 (12년~18년)",
    "B-클래스 W245 (05년~11년)"
  ],
  스프린터: [
    "스프린터 (95년~현재)"
  ],
  GLK클래스: [
    "GLK-클래스 X204 (09년~15년)"
  ],
  CLE클래스: [
    "CLE-클래스 C236 (24년~현재)"
  ],
  SLC클래스: [
    "SLC-클래스 R172 (16년~현재)"
  ],
  V클래스: [
    "V-클래스 (96년~현재)"
  ],
  CL클래스: [
    "CL-클래스 C216 (07년~13년)",
    "CL-클래스 C215 (99년~06년)",
    "CL-클래스 C140 (92년~99년)"
  ],
  EQC: [
    "EQC N293 (19년~현재)"
  ],
  CLK클래스: [
    "CLK-클래스 C209 (02년~09년)",
    "CLK-클래스 C208 (97년~03년)"
  ],
  SEL_SEC: [
    "SEL/SEC (72년~94년)"
  ],
  GL클래스: [
    "GL-클래스 X166 (12년~16년)",
    "GL-클래스 X164 (06년~12년)"
  ],
  SLS_AMG: [
    "SLS AMG (10년~14년)"
  ],
  R클래스: [
    "R-클래스 (05년~13년)"
  ],
  "190클래스": [
    "190-클래스 (82년~94년)"
  ],
  XC60: [
    "XC60 2세대 (17년~현재)",
    "XC60 (09년~17년)"
  ],
  XC90: [
    "XC90 2세대 (16년~현재)",
    "XC90 (03년~14년)"
  ],
  S90: [
    "S90 (16년~현재)"
  ],
  S60: [
    "S60 3세대 (19년~현재)",
    "S60 크로스컨트리 (15년~18년)",
    "S60 (00년~18년)"
  ],
  XC40: [
    "XC40 리차지 (22년~현재)",
    "XC40 (18년~현재)"
  ],
  V60: [
    "V60 크로스컨트리 2세대 (19년~현재)",
    "V60 크로스컨트리 (15년~18년)",
    "V60 (10년~18년)"
  ],
  V40: [
    "V40 크로스컨트리 (13년~현재)",
    "V40 (95년~19년)"
  ],
  V90: [
    "V90 크로스컨트리 (17년~현재)"
  ],
  S80: [
    "S80 (98년~16년)"
  ],
  C40: [
    "C40 리차지 (22년~현재)"
  ],
  XC70: [
    "XC70 (97년~16년)"
  ],
  C30: [
    "C30 (06년~13년)"
  ],
  S40: [
    "S40 (95년~12년)"
  ],
  S70: [
    "S70 (97년~00년)"
  ],
  940: [
    "940 (90년~98년)"
  ],
  V50: [
    "V50 (04년~12년)"
  ],
  C70: [
    "C70 (97년~13년)"
  ],
  EX30: [
    "EX30 (24년~현재)"
  ],
  V70: [
    "V70 (97년~12년)"
  ],
  740: [
    "740 (84년~92년)"
  ],
  760: [
    "760 (82년~90년)"
  ],
  850: [
    "850 (92년~97년)"
  ],
  960: [
    "960 (90년~98년)"
  ],
  A6: [
    "A6 (C8) (19년~현재)",
    "뉴 A6 (04년~18년)",
    "A6 (94년~04년)"
  ],
  A7: [
    "A7 (4K) (18년~현재)",
    "A7 (10년~17년)"
  ],
  A4: [
    "A4 (B9) (16년~현재)",
    "뉴 A4 (05년~16년)",
    "A4 (94년~05년)"
  ],
  A8: [
    "A8 (D5) (18년~현재)",
    "뉴 A8 (02년~17년)",
    "A8 (94년~02년)"
  ],
  Q5: [
    "Q5 (FY) (17년~현재)",
    "Q5 (08년~16년)"
  ],
  A5: [
    "A5 (F5) (17년~현재)",
    "A5 (07년~16년)"
  ],
  Q7: [
    "Q7 (4M) (16년~현재)",
    "Q7 (05년~15년)"
  ],
  Q8: [
    "Q8 (4M) (18년~현재)"
  ],
  A3: [
    "A3 (8Y) (22년~현재)",
    "뉴 A3 (03년~22년)",
    "A3 (96년~03년)"
  ],
  R8: [
    "R8 (4S) (16년~현재)",
    "R8 (06년~15년)"
  ],
  e트론: [
    "e-트론 (20년~24년)"
  ],
  Q3: [
    "Q3 (F3) (18년~현재)",
    "Q3 (11년~18년)"
  ],
  "Q4 e-트론": [
    "Q4 e-트론 (F4) (22년~현재)"
  ],
  S7: [
    "S7 (4K) (19년~현재)",
    "S7 (12년~17년)"
  ],
  S8: [
    "S8 (D5) (20년~현재)",
    "S8 (94년~17년)"
  ],
  TT: [
    "TT (8S) (14년~현재)",
    "뉴 TT (06년~14년)",
    "TT (98년~06년)"
  ],
  RS7: [
    "RS7 (4K) (21년~현재)",
    "RS7 (14년~17년)"
  ],
  S4: [
    "S4 (B9) (21년~현재)",
    "뉴 S4 (08년~16년)",
    "S4 (91년~08년)"
  ],
  S6: [
    "S6 (C8) (19년~현재)",
    "S6 (94년~18년)"
  ],
  SQ5: [
    "SQ5 (FY) (19년~현재)",
    "SQ5 (13년~17년)"
  ],
  RS5: [
    "RS5 (F5) (18년~현재)",
    "RS5 (10년~17년)"
  ],
  Q2: [
    "Q2 (17년~현재)"
  ],
  S3: [
    "S3 (8Y) (22년~현재)",
    "S3 (96년~22년)"
  ],
  TTS: [
    "TTS (8S) (15년~현재)",
    "TTS (08년~14년)"
  ],
  RSQ8: [
    "RSQ8 (4M) (20년~현재)"
  ],
  "e-트론 GT": [
    "e-트론 GT (21년~현재)"
  ],
  S5: [
    "S5 (F5) (18년~현재)",
    "S5 (07년~14년)"
  ],
  "RS e-트론 GT": [
    "RS e-트론 GT (21년~현재)"
  ],
  A1: [
    "A1 (10년~18년)"
  ],
  RS3: [
    "RS3 (8Y) (23년~현재)",
    "RS3 (03년~20년)"
  ],
  SQ8: [
    "SQ8 (4M) (20년~현재)"
  ],
  SQ7: [
    "SQ7 (4M) (23년~현재)"
  ],
  100: [
    "100 (68년~94년)"
  ],
  80: [
    "80 (72년~96년)"
  ],
  90: [
    "90 (78년~95년)"
  ],
  RS4: [
    "RS4 (00년~08년)"
  ],
  RS6: [
    "RS6 (C8) (21년~현재)",
    "RS6 (02년~18년)"
  ],
  TTRS: [
    "TTRS (8S) (16년~현재)",
    "TTRS (09년~14년)"
  ],
  V8: [
    "V8 (88년~94년)"
  ],
  "Q8 e-트론": [
    "Q8 e-트론 (GE) (24년~현재)"
  ],
  "SQ8 e-트론": [
    "SQ8 e-트론 (GE) (24년~현재)"
  ],
  "올로드 콰트로": [
    "올로드 콰트로 (99년~현재)"
  ],
  "모델 3": [
    "모델 3 (17년~현재)"
  ],
  "모델 Y": [
    "모델 Y (20년~현재)"
  ],
  "모델 X": [
    "모델 X (18년~현재)"
  ],
  "모델 S": [
    "모델 S (12년~현재)"
  ],
  카이엔: [
    "카이엔 (PO536) (19년~현재)",
    "뉴 카이엔 (10년~18년)",
    "카이엔 (02년~10년)"
  ],
  파나메라: [
    "파나메라 (972) (24년~현재)",
    "파나메라 (971) (17년~24년)",
    "파나메라 (09년~16년)"
  ],
  718: [
    "718 카이맨 (16년~현재)",
    "718 박스터 (16년~현재)"
  ],
  911: [
    "911 (992) (19년~현재)",
    "911 (89년~19년)"
  ],
  마칸: [
    "마칸 (14년~현재)"
  ],
  타이칸: [
    "타이칸 (20년~현재)"
  ],
  박스터: [
    "박스터 (96년~16년)"
  ],
  카이맨: [
    "카이맨 (05년~16년)"
  ],
  928: [
    "928 (77년~95년)"
  ],
  944: [
    "944 (82년~91년)"
  ],
  968: [
    "968 (92년~95년)"
  ],
  "카레라 GT": [
    "카레라 GT (04년~06년)"
  ],
  레인지로버: [
    "레인지로버 5세대 (22년~현재)",
    "레인지로버 4세대 (13년~22년)",
    "레인지로버 (70년~12년)"
  ],
  디스커버리: [
    "디스커버리 5 (17년~현재)",
    "디스커버리 4 (09년~16년)",
    "디스커버리 3 (04년~09년)",
    "디스커버리 2 (99년~05년)",
    "디스커버리 (89년~98년)"
  ],
  "디스커버리 스포츠": [
    "디스커버리 스포츠 2세대 (20년~현재)",
    "디스커버리 스포츠 (15년~19년)"
  ],
  "레인지로버 스포츠": [
    "레인지로버 스포츠 3세대 (22년~현재)",
    "레인지로버 스포츠 2세대 (13년~22년)",
    "레인지로버 스포츠 (04년~13년)"
  ],
  "레인지로버 이보크": [
    "레인지로버 이보크 2세대 (19년~현재)",
    "레인지로버 이보크 (11년~19년)"
  ],
  "레인지로버 벨라": [
    "레인지로버 벨라 (17년~현재)"
  ],
  디펜더: [
    "디펜더 (L663) (20년~현재)",
    "디펜더 (83년~16년)"
  ],
  프리랜더: [
    "프리랜더2 (06년~14년)",
    "프리랜더 (97년~06년)"
  ],
  리프: [
    "리프 (ZE1) (19년~현재)",
    "리프 (10년~18년)"
  ],
  알티마: [
    "알티마 (L34) (19년~현재)",
    "알티마 (93년~18년)"
  ],
  "370Z": [
    "370Z (09년~현재)"
  ],
  큐브: [
    "큐브 (98년~19년)"
  ],
  맥시마: [
    "맥시마 (A36) (15년~현재)",
    "맥시마 (76년~14년)"
  ],
  쥬크: [
    "쥬크 (11년~현재)"
  ],
  무라노: [
    "무라노 (Z52) (15년~현재)",
    "무라노 (02년~14년)"
  ],
  패스파인더: [
    "패스파인더 4세대 (13년~현재)",
    "패스파인더 (86년~12년)"
  ],
  엑스트레일: [
    "엑스트레일 (19년~현재)"
  ],
  로그: [
    "로그 (T32) (14년~20년)",
    "로그 (S35) (07년~13년)"
  ],
  스카이라인: [
    "스카이라인 (81년~현재)"
  ],
  캐시카이: [
    "캐시카이 2세대 (14년~현재)"
  ],
  "350Z": [
    "350Z (03년~09년)"
  ],
  "GT-R": [
    "GT-R (07년~현재)"
  ],
  마치: [
    "마치 (82년~현재)"
  ],
  휘가로: [
    "휘가로 (91년~91년)"
  ],
  프론티어: [
    "프론티어 (97년~현재)"
  ],
  NV: [
    "NV (11년~현재)"
  ],
  노트: [
    "노트 (05년~현재)"
  ],
  로렐: [
    "로렐 (68년~02년)"
  ],
  모코: [
    "모코 (02년~현재)"
  ],
  버사: [
    "버사 (04년~현재)"
  ],
  베르사: [
    "베르사 (07년~현재)"
  ],
  "블루버드 실피": [
    "블루버드 실피 (00년~12년)"
  ],
  블루버드: [
    "블루버드 (57년~01년)"
  ],
  세드릭: [
    "세드릭 (60년~04년)"
  ],
  MKZ: [
    "뉴 MKZ (10년~현재)",
    "MKZ (05년~09년)"
  ],
  에비에이터: [
    "에비에이터 2세대 (19년~현재)",
    "에비에이터 (02년~05년)"
  ],
  MKS: [
    "뉴 MKS (12년~16년)",
    "MKS (08년~12년)"
  ],
  컨티넨탈: [
    "컨티넨탈 10세대 (16년~현재)",
    "컨티넨탈 (80년~02년)"
  ],
  네비게이터: [
    "네비게이터 (97년~현재)"
  ],
  MKX: [
    "MKX 2세대 (15년~18년)",
    "뉴 MKX (10년~15년)",
    "MKX (06년~10년)"
  ],
  노틸러스: [
    "노틸러스 2세대 (23년~현재)",
    "노틸러스 (19년~23년)"
  ],
  MKC: [
    "MKC (14년~현재)"
  ],
  코세어: [
    "코세어 (20년~현재)"
  ],
  타운카: [
    "타운카 (81년~11년)"
  ],
  LS: [
    "LS (99년~06년)"
  ],
  MKT: [
    "MKT (09년~현재)"
  ],
  포커스: [
    "포커스 (98년~현재)"
  ],
  익스플로러: [
    "익스플로러 6세대 (19년~현재)",
    "익스플로러 (91년~19년)"
  ],
  머스탱: [
    "머스탱 7세대 (24년~현재)",
    "머스탱 (64년~24년)"
  ],
  F150: [
    "F150 (73년~현재)"
  ],
  티구안: [
    "티구안 올스페이스 (18년~현재)",
    "티구안 2세대 (18년~현재)",
    "뉴 티구안 (11년~16년)",
    "티구안 (07년~11년)"
  ],
  골프: [
    "골프 8세대 (22년~현재)",
    "골프 7세대 (13년~19년)",
    "골프 6세대 (08년~14년)",
    "골프 5세대 (04년~09년)",
    "골프 4세대 (97년~04년)",
    "골프 3세대 (91년~99년)",
    "골프 2세대 (83년~92년)",
    "골프 1세대 (74년~83년)"
  ],
  아테온: [
    "아테온 (18년~현재)"
  ],
  제타: [
    "제타 7세대 (19년~현재)",
    "뉴 제타 (11년~18년)",
    "제타 (79년~11년)"
  ],
  파사트: [
    "파사트 GT (B8) (18년~현재)",
    "더 뉴 파사트 (11년~현재)",
    "뉴 파사트 (05년~11년)",
    "파사트 (73년~05년)",
    "파사트 바리안트 (73년~현재)"
  ],
  CC: [
    "뉴 CC (12년~17년)",
    "CC (08년~12년)"
  ],
  투아렉: [
    "투아렉 3세대 (19년~현재)",
    "뉴 투아렉 (10년~18년)",
    "투아렉 (02년~10년)"
  ],
  비틀: [
    "더 비틀 (12년~19년)",
    "뉴 비틀 (98년~12년)",
    "비틀 (38년~03년)"
  ],
  폴로: [
    "폴로 (75년~현재)"
  ],
  시로코: [
    "시로코 (08년~17년)"
  ],
  티록: [
    "티록 (21년~현재)"
  ],
  페이톤: [
    "페이톤 (02년~16년)"
  ],
  "ID.4": [
    "ID.4 (22년~현재)"
  ],
  쿠퍼: [
    "쿠퍼 일렉트릭 (22년~현재)",
    "쿠퍼 SD (12년~현재)",
    "쿠퍼 D (07년~현재)",
    "쿠퍼 (01년~현재)",
    "쿠퍼 S (01년~현재)"
  ],
  컨트리맨: [
    "쿠퍼 D 컨트리맨 (11년~현재)",
    "쿠퍼 SD 컨트리맨 (11년~현재)",
    "쿠퍼 컨트리맨 (11년~현재)",
    "쿠퍼 S 컨트리맨 (11년~현재)"
  ],
  클럽맨: [
    "쿠퍼 SD 클럽맨 (13년~현재)",
    "쿠퍼 D 클럽맨 (09년~현재)",
    "쿠퍼 클럽맨 (07년~현재)",
    "쿠퍼 S 클럽맨 (07년~현재)"
  ],
  "쿠퍼 컨버터블": [
    "쿠퍼 컨버터블 (01년~현재)",
    "쿠퍼 S 컨버터블 (01년~현재)"
  ],
  쿠페: [
    "쿠퍼 SD 쿠페 (12년~15년)",
    "쿠퍼 쿠페 (11년~15년)",
    "쿠퍼 S 쿠페 (11년~15년)"
  ],
  페이스맨: [
    "쿠퍼 D 페이스맨 (13년~현재)",
    "쿠퍼 SD 페이스맨 (13년~현재)"
  ],
  로드스터: [
    "쿠퍼 로드스터 (12년~15년)",
    "쿠퍼 S 로드스터 (12년~15년)"
  ],
  "로버 미니": [
    "로버 미니 (76년~01년)"
  ],
  에스컬레이드: [
    "에스컬레이드 5세대 (21년~현재)",
    "에스컬레이드 (99년~20년)"
  ],
  CT6: [
    "CT6 (16년~현재)"
  ],
  CTS: [
    "CTS 3세대 (14년~19년)",
    "CTS 2세대 (08년~14년)",
    "CTS 1세대 (02년~07년)"
  ],
  ATS: [
    "ATS (13년~19년)"
  ],
  XT5: [
    "XT5 (16년~현재)"
  ],
  캠리: [
    "캠리 (XV70) (17년~현재)",
    "뉴 캠리 (12년~17년)",
    "캠리 (86년~11년)"
  ],
  프리우스: [
    "프리우스 5세대 (23년~현재)",
    "프리우스 C (18년~21년)",
    "프리우스 프라임 (17년~현재)",
    "프리우스 4세대 (16년~23년)",
    "프리우스 V (12년~21년)",
    "프리우스 (97년~15년)"
  ],
  RAV4: [
    "RAV4 5세대 (19년~현재)",
    "RAV4 (94년~18년)"
  ],
  시에나: [
    "시에나 4세대 (20년~현재)",
    "시에나 (98년~20년)"
  ],
  86: [
    "GR86 (22년~현재)",
    "86 (12년~현재)"
  ],
  알파드: [
    "알파드 4세대 (23년~현재)",
    "알파드 (02년~22년)"
  ],
  크라운: [
    "크라운 크로스오버 (23년~현재)",
    "크라운 마제스타 (91년~현재)",
    "크라운 (79년~현재)"
  ],
  "FJ 크루져": [
    "FJ 크루져 (06년~14년)"
  ],
  ES: [
    "ES300h 7세대 (18년~현재)",
    "뉴 ES350 (12년~18년)",
    "뉴 ES300h (12년~18년)",
    "ES350 (06년~12년)",
    "ES330 (01년~06년)",
    "ES300 (91년~06년)"
  ],
  NX: [
    "NX450h+ 2세대 (22년~현재)",
    "NX350h 2세대 (22년~현재)",
    "NX300 (17년~21년)",
    "NX200t (15년~17년)",
    "NX300h (14년~21년)"
  ],
  RX: [
    "RX350h 5세대 (23년~현재)",
    "RX450h+ 5세대 (23년~현재)",
    "RX500h 5세대 (23년~현재)",
    "RX450hL 4세대 (20년~23년)",
    "RX350 4세대 (16년~23년)",
    "RX450h 4세대 (16년~23년)",
    "RX450h (09년~15년)",
    "RX400h (03년~09년)",
    "RX330 (03년~09년)",
    "RX350 (97년~15년)",
    "RX300 (97년~03년)"
  ],
  LS: [
    "LS500 5세대 (18년~현재)",
    "LS500h 5세대 (17년~현재)",
    "LS600hL (06년~17년)",
    "LS460L (06년~17년)",
    "LS460 (06년~17년)",
    "LS430 (00년~06년)",
    "LS400 (89년~00년)"
  ],
  UX: [
    "UX300e (22년~현재)",
    "UX250h (19년~현재)"
  ],
  CT200h: [
    "CT200h (10년~현재)"
  ],
  IS: [
    "뉴 IS300 (17년~21년)",
    "뉴 IS200t (15년~17년)",
    "뉴 IS250 (13년~15년)",
    "IS F (07년~14년)",
    "IS250 (05년~13년)",
    "IS350 (05년~13년)",
    "IS200 (98년~05년)",
    "IS300 (98년~13년)"
  ],
  GS: [
    "뉴 GS300 (17년~현재)",
    "뉴 GS200t (16년~17년)",
    "뉴 GS F (16년~현재)",
    "뉴 GS250 (12년~16년)",
    "뉴 GS350 (12년~현재)",
    "뉴 GS450h (12년~현재)",
    "GS460 (05년~12년)",
    "GS350 (97년~12년)",
    "GS400 (97년~05년)",
    "GS430 (97년~12년)",
    "GS450h (97년~12년)",
    "GS300 (91년~12년)"
  ],
  RC: [
    "RC300 (19년~현재)",
    "RC200t (16년~현재)",
    "RC350 (15년~현재)",
    "RC F (15년~현재)"
  ],
  RZ: [
    "RZ450e (23년~현재)"
  ],
  LC: [
    "LC (17년~현재)"
  ],
  SC: [
    "SC430 (01년~10년)",
    "SC300 (91년~00년)"
  ],
  GX: [
    "GX460 (09년~현재)",
    "GX470 (02년~09년)"
  ],
  LX: [
    "LX (96년~현재)"
  ],
  라피드:[
    "라피드 (10년~현재)"
  ],
  기블리: [
    "기블리 (13년~현재)"
  ],
  르반떼: [
    "르반떼 (16년~현재)"
  ],
  콰트로포르테: [
    "콰트로포르테 (63년~현재)"
  ],
  그란투리스모: [
    "그란투리스모 (07년~현재)"
  ],
  3008: [
    "3008 2세대 (17년~현재)",
    "3008 (09년~16년)"
  ],
  2008: [
    "2008 2세대 (20년~현재)",
    "e-2008 2세대 (20년~현재)",
    "2008 (13년~20년)"
  ],
  508: [
    "508SW 2세대 (19년~현재)",
    "508 2세대 (19년~현재)",
    "508 RXH (14년~18년)",
    "508 (11년~18년)",
    "508SW (11년~18년)"
  ],
  5008: [
    "5008 2세대 (17년~현재)",
    "5008 1세대 (09년~16년)"
  ],
  랭글러: [
    "랭글러 (JL) (18년~현재)",
    "랭글러 (JK) (07년~18년)",
    "랭글러 (TJ) (96년~06년)",
    "랭글러 (YJ) (87년~95년)"
  ],
  체로키: [
    "그랜드 체로키(WL) (21년~현재)",
    "체로키(KL) (14년~현재)",
    "그랜드 체로키 (93년~22년)",
    "체로키 (84년~13년)"
  ],
  레니게이드: [
    "레니게이드 (15년~현재)"
  ],
  글래디에이터: [
    "글래디에이터 (JT) (20년~현재)"
  ],
  컴패스: [
    "컴패스 2세대 (18년~현재)",
    "컴패스 (07년~17년)"
  ],
  커맨더: [
    "커맨더 (06년~10년)"
  ],
  어코드: [
    "어코드 11세대 (23년~현재)",
    "어코드 10세대 (18년~23년)",
    "올뉴어코드 (08년~17년)",
    "어코드 (76년~07년)"
  ],
  XF: [
    "XF (X260) (16년~현재)",
    "New XF (11년~15년)",
    "XF (08년~11년)"
  ],
  XJ: [
    "All New XJ (10년~현재)",
    "New XJ (68년~09년)"
  ],
  XE: [
    "XE (15년~현재)"
  ],
  "F-PACE": [
    "F-PACE (16년~현재)"
  ],
  "F-TYPE": [
    "F-TYPE (13년~현재)"
  ],
  "E-PACE": [
    "E-PACE (18년~현재)"
  ],
  Q50: [
    "Q50 (14년~현재)"
  ],
  QX60: [
    "QX60 (14년~현재)"
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
const recentSearchImportedCondition = ref(JSON.parse(sessionStorage.getItem('recentSearchImportedCondition')) || []);

// 최근 검색조건에 추가하는 함수
const addrecentSearchImportedCondition = () => {
  if (selectedManufacturer.value && selectedModel.value) {
    // 중복된 검색 조건인지 확인
    const existingCondition = recentSearchImportedCondition.value.find(
      (condition) => condition.manufacturer === selectedManufacturer.value && condition.model === selectedModel.value
    );

    if (!existingCondition) {
      // 최근 검색 조건이 5개를 초과하면 가장 오래된 조건을 제거
      if (recentSearchImportedCondition.value.length >= 5) {
        recentSearchImportedCondition.value.shift(); // 가장 오래된 조건 제거
      }

      // 새로운 검색 조건 추가
      recentSearchImportedCondition.value.push({
        manufacturer: selectedManufacturer.value,
        model: selectedModel.value,
      });
      sessionStorage.setItem('recentSearchImportedCondition', JSON.stringify(recentSearchImportedCondition.value));
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
        addrecentSearchImportedCondition();
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

  const url = `${process.env.API}products?page=${search.value.page}&limit=${search.value.limit}&manufacturers=${search.value.manufacturers}&types=${search.value.types}&name=${search.value.name}&min_year=${search.value.min_year}&max_year=${search.value.max_year}&min_distance=${search.value.min_distance}&max_distance=${search.value.max_distance}&min_price=${search.value.min_price}&max_price=${search.value.max_price}&grade=${search.value.grade}&category=imported`;

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

const importedProductCount = ref(0);
const GetImportedProductCount = () => {

  const url = `${process.env.API}count_products?category=imported`;

  api.get(url)
    .then((res) => {
      console.log("국산차 수량 확인", res.data);
      importedProductCount.value = res.data.count;
    })
    .catch((err) => {
      console.log(err);
    });
};

const createNrefresh = (id) => {
  createInterestProduct(id);
  GetUserInterestProduct();
}

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
  recentSearchImportedCondition.value = [];
  sessionStorage.removeItem('recentSearchImportedCondition');
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
  GetImportedProductCount();
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
  max-height: 400px;
  overflow-y: auto;
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
