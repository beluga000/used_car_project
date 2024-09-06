<template>
  <q-layout class="page-container page-background">
    <q-page class="common-container-1">
      <div class="main-container">
        <q-card flat bordered class="q-pa-md">
          <q-card-section>
            <div class="text-h5 q-mb-md">차량 이미지 등록</div>

            <!-- 이미지 업로더 -->
            <q-uploader
              url="http://localhost:4444/upload"
              label="차량 이미지 등록"
              multiple
              @added="onFilesAdded"
              @removed="onFileRemoved"
              @removedAll="onAllFilesRemoved"
              accept="image/*"
              color="red-6"
            >
              <template v-slot:header="scope">
                <div class="row no-wrap items-center q-pa-sm q-gutter-xs">
                  <q-btn
                    v-if="scope.queuedFiles.length > 0"
                    icon="clear_all"
                    @click="() => { scope.removeQueuedFiles(); onAllFilesRemoved(); }"
                    round
                    dense
                    flat
                  >
                    <q-tooltip>Clear All</q-tooltip>
                  </q-btn>
                  <q-btn
                    v-if="scope.uploadedFiles.length > 0"
                    icon="done_all"
                    @click="() => { scope.removeUploadedFiles(); onAllFilesRemoved(); }"
                    round
                    dense
                    flat
                  >
                    <q-tooltip>Remove Uploaded Files</q-tooltip>
                  </q-btn>
                  <q-spinner
                    v-if="scope.isUploading"
                    class="q-uploader__spinner"
                  />
                  <div class="col">
                    <div class="q-uploader__title">
                      + 버튼을 눌러 차량 사진을 등록해주세요.
                    </div>
                    <div class="q-uploader__subtitle">
                      {{ scope.uploadSizeLabel }} / {{ scope.uploadProgressLabel }}
                    </div>
                  </div>
                  <q-btn
                    v-if="scope.canAddFiles"
                    type="a"
                    icon="add_box"
                    @click="scope.pickFiles"
                    round
                    dense
                    flat
                  >
                    <q-uploader-add-trigger />
                    <q-tooltip>Pick Files</q-tooltip>
                  </q-btn>
                  <q-btn
                    v-if="scope.canUpload"
                    icon="cloud_upload"
                    @click="scope.upload"
                    round
                    dense
                    flat
                  >
                    <q-tooltip>Upload Files</q-tooltip>
                  </q-btn>
                  <q-btn
                    v-if="scope.isUploading"
                    icon="clear"
                    @click="scope.abort"
                    round
                    dense
                    flat
                  >
                    <q-tooltip>Abort Upload</q-tooltip>
                  </q-btn>
                </div>
              </template>
            </q-uploader>

            <!-- 썸네일 미리보기 -->
            <div class="q-gutter-md q-mt-md row q-col-gutter-md q-col-6 q-col-sm-4 q-col-md-3">
              <div
                v-for="(image, index) in imagePreviews"
                :key="image.id"
                class="col-6 col-sm-4 col-md-3"
              >
                <q-img
                  :src="image.url"
                  :alt="'차량 이미지 ' + (index + 1)"
                  style="max-height: 100px;"
                  class="full-width"
                />
              </div>
            </div>

          </q-card-section>
        </q-card>

        <q-card flat bordered class="q-pa-md">
          <q-card-section>
            <div class="text-h5 q-mb-md">차량 판매글 작성</div>

            <!-- 차량 기본 정보 -->
            <div class="q-gutter-md">
              <div class="btn-line">
                <q-btn
                  class="category-btn"
                  :class="{ active: activeButton === idx }"
                  v-for="(item, idx) in ManufactuerOptions"
                  :key="idx"
                  @click="selectManufacturer(item, idx)"
                >
                  {{ item }}
                </q-btn>
              </div>
              <q-select
                v-model="car.company"
                :options="CompanyOptions"
                label="제조사 선택"
                outlined
                @update:model-value="onCompanyChange"
              />
              <q-select
                v-model="car.model"
                :options="ModelOptions"
                label="모델 선택"
                outlined
                @update:model-value="onModelChange"
              />
              <q-select
                v-model="car.grade"
                :options="GradeOptions"
                label="세부모델 선택"
                outlined
              />
              <q-input v-model="car.price" label="판매 가격 (만원)" outlined />
              <q-input v-model="car.registration" label="차량 등록 번호" outlined />
              <q-input v-model="car.mileage" label="주행거리 (km)" outlined />
              <q-select v-model="car.fuelType" :options="fuelOptions" label="연료 종류" outlined />
              <q-select v-model="car.transmission" :options="transmissionOptions" label="변속기" outlined />
              <q-input
                v-model="formattedYear"
                label="연식 (년/월)"
                outlined
                @input="formatYear"
              />
              <q-input v-model="car.color" label="차량 색상" outlined />

              <!-- 차량 옵션 -->
              <q-card-section>
                <div class="text-h6 q-mb-md">차량 외관옵션</div>

                <q-expansion-item v-model="isOptionsExpanded" icon="directions_car" label="차량 외관 옵션" expand-separator>
                <div class="q-gutter-md">
                  <q-checkbox v-model="carOptions[0]" @update:model-value="updateOptions" label="HID 램프" />
                  <q-checkbox v-model="carOptions[1]" @update:model-value="updateOptions" label="LED 램프" />
                  <q-checkbox v-model="carOptions[2]" @update:model-value="updateOptions" label="어댑티브 램프" />
                  <q-checkbox v-model="carOptions[3]" @update:model-value="updateOptions" label="하이빔" />
                  <q-checkbox v-model="carOptions[4]" @update:model-value="updateOptions" label="전동 접이 사이드미러" />
                  <q-checkbox v-model="carOptions[5]" @update:model-value="updateOptions" label="열선 사이드미러" />
                  <q-checkbox v-model="carOptions[6]" @update:model-value="updateOptions" label="후진 각도조절 사이드미러" />
                  <q-checkbox v-model="carOptions[7]" @update:model-value="updateOptions" label="썬루프" />
                  <q-checkbox v-model="carOptions[8]" @update:model-value="updateOptions" label="듀얼 썬루프" />
                  <q-checkbox v-model="carOptions[9]" @update:model-value="updateOptions" label="파노라마 썬루프" />
                  <q-checkbox v-model="carOptions[10]" @update:model-value="updateOptions" label="와이퍼 결빙방지 윈드실드" />
                  <q-checkbox v-model="carOptions[11]" @update:model-value="updateOptions" label="자외선 차단 윈드실드" />
                  <q-checkbox v-model="carOptions[12]" @update:model-value="updateOptions" label="알루미늄휠" />
                  <q-checkbox v-model="carOptions[13]" @update:model-value="updateOptions" label="크롬휠" />
                  <q-checkbox v-model="carOptions[14]" @update:model-value="updateOptions" label="광폭타이어" />
                </div>
              </q-expansion-item>

              <q-expansion-item v-model="isOptionsExpanded_in" icon="directions_car" label="차량 내장 옵션" expand-separator>
                <div class="q-gutter-md">
                  <q-checkbox v-model="CarInOptions[0]" @update:model-value="updateInOptions" label="가죽스티어링휠" />
                  <q-checkbox v-model="CarInOptions[1]" @update:model-value="updateInOptions" label="우드스티어링휠" />
                  <q-checkbox v-model="CarInOptions[2]" @update:model-value="updateInOptions" label="열선내장 스티어링 휠" />
                  <q-checkbox v-model="CarInOptions[3]" @update:model-value="updateInOptions" label="직물시트" />
                  <q-checkbox v-model="CarInOptions[4]" @update:model-value="updateInOptions" label="가죽시트" />
                  <q-checkbox v-model="CarInOptions[5]" @update:model-value="updateInOptions" label="전동시트(운전석)" />
                  <q-checkbox v-model="CarInOptions[6]" @update:model-value="updateInOptions" label="전동시트(동승석)" />
                  <q-checkbox v-model="CarInOptions[7]" @update:model-value="updateInOptions" label="전동시트(뒷좌석)" />
                  <q-checkbox v-model="CarInOptions[8]" @update:model-value="updateInOptions" label="열선시트(앞)" />
                  <q-checkbox v-model="CarInOptions[9]" @update:model-value="updateInOptions" label="열선시트(뒤)" />
                  <q-checkbox v-model="CarInOptions[10]" @update:model-value="updateInOptions" label="메모리시트(운전석)" />
                  <q-checkbox v-model="CarInOptions[11]" @update:model-value="updateInOptions" label="메모리시트(동승석)" />
                  <q-checkbox v-model="CarInOptions[12]" @update:model-value="updateInOptions" label="통풍시트(운전석)" />
                  <q-checkbox v-model="CarInOptions[13]" @update:model-value="updateInOptions" label="통풍시트(동승석)" />
                  <q-checkbox v-model="CarInOptions[14]" @update:model-value="updateInOptions" label="안마시트" />
                  <q-checkbox v-model="CarInOptions[15]" @update:model-value="updateInOptions" label="ECM 룸미러" />
                  <q-checkbox v-model="CarInOptions[16]" @update:model-value="updateInOptions" label="하이패스내장 룸미러" />
                  <q-checkbox v-model="CarInOptions[17]" @update:model-value="updateInOptions" label="후방룸미러" />
                  <q-checkbox v-model="CarInOptions[18]" @update:model-value="updateInOptions" label="풋파킹 브레이크" />
                  <q-checkbox v-model="CarInOptions[19]" @update:model-value="updateInOptions" label="전자식파킹 브레이크" />
                </div>
              </q-expansion-item>

              <q-expansion-item v-model="isOptionsExpanded_save" icon="directions_car" label="차량 안전 옵션" expand-separator>
                <div class="q-gutter-md">
                  <q-checkbox v-model="CarSaveOptions[0]" @update:model-value="updateSaveOptions" label="운전석에어백" />
                  <q-checkbox v-model="CarSaveOptions[1]" @update:model-value="updateSaveOptions" label="동승석에어백" />
                  <q-checkbox v-model="CarSaveOptions[2]" @update:model-value="updateSaveOptions" label="사이드에어백" />
                  <q-checkbox v-model="CarSaveOptions[3]" @update:model-value="updateSaveOptions" label="커튼에어백" />
                  <q-checkbox v-model="CarSaveOptions[4]" @update:model-value="updateSaveOptions" label="무릎보호에어백" />
                  <q-checkbox v-model="CarSaveOptions[5]" @update:model-value="updateSaveOptions" label="전방감지센서" />
                  <q-checkbox v-model="CarSaveOptions[6]" @update:model-value="updateSaveOptions" label="후방감지센서" />
                  <q-checkbox v-model="CarSaveOptions[7]" @update:model-value="updateSaveOptions" label="전방카메라" />
                  <q-checkbox v-model="CarSaveOptions[8]" @update:model-value="updateSaveOptions" label="후방카메라" />
                  <q-checkbox v-model="CarSaveOptions[9]" @update:model-value="updateSaveOptions" label="차선이탈방지(LDWS)" />
                  <q-checkbox v-model="CarSaveOptions[10]" @update:model-value="updateSaveOptions" label="어라운드뷰(AVM)" />
                  <q-checkbox v-model="CarSaveOptions[11]" @update:model-value="updateSaveOptions" label="후측방경보시스템(BSD/BSW)" />
                  <q-checkbox v-model="CarSaveOptions[12]" @update:model-value="updateSaveOptions" label="ABS 브레이크 잠김방지" />
                  <q-checkbox v-model="CarSaveOptions[13]" @update:model-value="updateSaveOptions" label="TCS 미끄럼방지" />
                  <q-checkbox v-model="CarSaveOptions[14]" @update:model-value="updateSaveOptions" label="VDC(ESP) 차체자세 제어" />
                  <q-checkbox v-model="CarSaveOptions[15]" @update:model-value="updateSaveOptions" label="ECS 전자제어서스펜션" />
                  <q-checkbox v-model="CarSaveOptions[16]" @update:model-value="updateSaveOptions" label="ESS 급제동경보시스템" />
                  <q-checkbox v-model="CarSaveOptions[17]" @update:model-value="updateSaveOptions" label="HAS 경사로" />
                  <q-checkbox v-model="CarSaveOptions[18]" @update:model-value="updateSaveOptions" label="TPMS 타이어공기압" />
                  <q-checkbox v-model="CarSaveOptions[19]" @update:model-value="updateSaveOptions" label="유아시트고정장치" />
                  <q-checkbox v-model="CarSaveOptions[20]" @update:model-value="updateSaveOptions" label="세이프티윈도우" />
                  <q-checkbox v-model="CarSaveOptions[21]" @update:model-value="updateSaveOptions" label="액티브헤드레스트" />
                  <q-checkbox v-model="CarSaveOptions[22]" @update:model-value="updateSaveOptions" label="전동식파워스티어링" />
                  <q-checkbox v-model="CarSaveOptions[23]" @update:model-value="updateSaveOptions" label="AGCS 주행안정성 제어 시스템" />
                </div>
              </q-expansion-item>

              <q-expansion-item v-model="isOptionsExpanded_conv" icon="directions_car" label="차량 편의 옵션" expand-separator>
                <div class="q-gutter-md">
                  <q-checkbox v-model="CarConOptions[0]" @update:model-value="updateConOptions" label="에어컨" />
                  <q-checkbox v-model="CarConOptions[1]" @update:model-value="updateConOptions" label="풀오토 에어컨" />
                  <q-checkbox v-model="CarConOptions[2]" @update:model-value="updateConOptions" label="듀얼 풀오토 에어컨" />
                  <q-checkbox v-model="CarConOptions[3]" @update:model-value="updateConOptions" label="CD" />
                  <q-checkbox v-model="CarConOptions[4]" @update:model-value="updateConOptions" label="CD 체인저" />
                  <q-checkbox v-model="CarConOptions[5]" @update:model-value="updateConOptions" label="DVD" />
                  <q-checkbox v-model="CarConOptions[6]" @update:model-value="updateConOptions" label="AUX단자" />
                  <q-checkbox v-model="CarConOptions[7]" @update:model-value="updateConOptions" label="MP3" />
                  <q-checkbox v-model="CarConOptions[8]" @update:model-value="updateConOptions" label="USB" />
                  <q-checkbox v-model="CarConOptions[9]" @update:model-value="updateConOptions" label="iPod" />
                  <q-checkbox v-model="CarConOptions[10]" @update:model-value="updateConOptions" label="네비게이션" />
                  <q-checkbox v-model="CarConOptions[11]" @update:model-value="updateConOptions" label="스마트키" />
                  <q-checkbox v-model="CarConOptions[12]" @update:model-value="updateConOptions" label="버튼시동" />
                  <q-checkbox v-model="CarConOptions[13]" @update:model-value="updateConOptions" label="크루즈컨트롤" />
                  <q-checkbox v-model="CarConOptions[14]" @update:model-value="updateConOptions" label="핸즈프리" />
                  <q-checkbox v-model="CarConOptions[15]" @update:model-value="updateConOptions" label="전동식 파워 트렁크" />
                  <q-checkbox v-model="CarConOptions[16]" @update:model-value="updateConOptions" label="자동주차시스템" />
                  <q-checkbox v-model="CarConOptions[17]" @update:model-value="updateConOptions" label="레인센서와이퍼" />
                  <q-checkbox v-model="CarConOptions[18]" @update:model-value="updateConOptions" label="속도 감응식 스티어링휠" />
                  <q-checkbox v-model="CarConOptions[19]" @update:model-value="updateConOptions" label="스티어링휠 리모컨" />
                  <q-checkbox v-model="CarConOptions[20]" @update:model-value="updateConOptions" label="트립컴퓨터" />
                </div>
              </q-expansion-item>
              </q-card-section>

              <!-- 차량 설명
              <q-card-section>
                <q-input
                  v-model="car.description"
                  label="차량 설명"
                  type="textarea"
                  rows="5"
                  outlined
                />
              </q-card-section> -->

              <!-- 제출 버튼 -->
              <q-btn label="등록하기" type="submit" color="red-6" class="full-width" @click="submitProduct()" />
            </div>
          </q-card-section>
        </q-card>
      </div>
    </q-page>
  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useQuasar } from "quasar";
import { api } from "boot/axios";

// 기본 세팅
const $router = useRouter();
const route = useRoute();
const $q = useQuasar();

// 차량 정보 객체
const car = ref({
  model: '',
  grade: '',
  company: '',
  price: '',
  registration: '',
  mileage: '',
  fuelType: '',
  transmission: '',
  year: '',
  color: '',
  img:[],
  o_in_options: [],
  o_out_options: [],
  o_con_options: [],
  o_save_options: [],
  out_options:["HID 램프", "LED 램프", "어댑티브 램프", "하이빔", "전동 접이 사이드미러", "열선 사이드미러", "후진 각도조절 사이드미러", "썬루프", "듀얼 썬루프", "파노라마 썬루프", "와이퍼 결빙방지 윈드실드", "자외선 차단 윈드실드", "알루미늄휠", "크롬휠", "광폭타이어"],
  in_options:["가죽스티어링휠", "우드스티어링휠", "열선내장 스티어링 휠", "직물시트", "가죽시트", "전동시트(운전석)", "전동시트(동승석)", "전동시트(뒷좌석)", "열선시트(앞)", "열선시트(뒤)", "메모리시트(운전석)", "메모리시트(동승석)", "통풍시트(운전석)", "통풍시트(동승석)", "안마시트", "ECM 룸미러", "하이패스내장 룸미러", "후방룸미러", "풋파킹 브레이크", "전자식파킹 브레이크"],
  save_options:["운전석에어백", "동승석에어백", "사이드에어백", "커튼에어백", "무릎보호에어백", "전방감지센서", "후방감지센서", "전방카메라", "후방카메라", "차선이탈방지(LDWS)", "어라운드뷰(AVM)", "후측방경보시스템(BSD/BSW)", "ABS 브레이크 잠김방지", "TCS 미끄럼방지", "VDC(ESP) 차체자세 제어", "ESS 급제동경보시스템", "HAS 경사로", "TPMS 타이어공기압", "유아시트고정장치", "세이프티윈도우", "액티브헤드레스트", "전동식파워스티어링", "AGCS 주행안정성 제어 시스템"],
  con_options:["에어컨", "풀오토 에어컨", "듀얼 풀오토 에어컨", "CD", "CD 체인저", "DVD", "AUX단자", "MP3", "USB", "iPod", "네비게이션", "스마트키", "버튼시동", "크루즈컨트롤", "핸즈프리", "전동식 파워 트렁크", "자동주차시스템", "레인센서와이퍼", "속도 감응식 스티어링휠", "스티어링휠 리모컨", "트립컴퓨터"]
});

const formattedYear = ref('2024/01');

const formatYear = (value) => {
  // 숫자 이외의 문자 제거
  let currentValue = value.replace(/[^\d]/g, '');

  // 연도와 월을 추출 (YYYYMM 형식이므로 6글자까지 허용)
  let year = currentValue.slice(0, 4);
  let month = currentValue.slice(4, 6);

  // 월의 범위가 1~12 사이인지 확인하고 조정
  if (month.length === 1) {
    month = '0' + month; // 월이 1자리일 경우 앞에 0을 붙임
  } else if (month.length === 2 && (parseInt(month, 10) < 1 || parseInt(month, 10) > 12)) {
    month = '01'; // 잘못된 월 입력 시 01로 고정
  }

  // 완성된 형식: YYYY/MM
  formattedYear.value = year + (month ? '/' + month : '');

  // car.year에 저장
  car.value.year = formattedYear.value;
};

// 차량 외장 옵션
const carOptions = ref(Array(15).fill(false)); // 15개의 옵션
const updateOptions = () => {
      car.value.o_out_options = [...carOptions.value]; // carOptions 배열을 복사하여 in_options에 저장
    };
// 차량 내장 옵션
const CarInOptions = ref(Array(20).fill(false)); // 20개의 옵션
const updateInOptions = () => {
  car.value.o_in_options = [...CarInOptions.value]; // CarInOptions 배열을 복사하여 in_options에 저장
};
// 차량 안전 옵션
const CarSaveOptions = ref(Array(24).fill(false)); // 10개의 옵션
const updateSaveOptions = () => {
  car.value.o_save_options = [...CarSaveOptions.value]; // CarSaveOptions 배열을 복사하여 in_options에 저장
};
// 차량 편의 옵션
const CarConOptions = ref(Array(21).fill(false)); // 10개의 옵션
const updateConOptions = () => {
  car.value.o_con_options = [...CarConOptions.value]; // CarConOptions 배열을 복사하여 in_options에 저장
};

// 선택된 제조사 추적
const selectedManufacturer = ref('');
const isOptionsExpanded = ref(false); // 옵션 섹션 열림/닫힘 상태 관리
const isOptionsExpanded_in = ref(false); // 옵션 섹션 열림/닫힘 상태 관리
const isOptionsExpanded_save = ref(false); // 옵션 섹션 열림/닫힘 상태 관리
const isOptionsExpanded_conv = ref(false); // 옵션 섹션 열림/닫힘 상태 관리

// 연료 옵션 리스트
const fuelOptions = ref([
  '가솔린', '디젤', 'LPG', '하이브리드', '전기'
]);

const ManufactuerOptions = ref([
  '국산', '수입'
]);

const CompanyOptions = ref([]);
const ModelOptions = ref([]);
const GradeOptions = ref([]);

const carData = {
  현대: {
    models: ["그랜저", "아반떼", "쏘나타", "싼타페", "스타렉스", "투싼", "펠리세이드", "제네시스",
    "코나", "에쿠스", "스타리아", "캐스퍼", "아이오닉5", "엑센트", "i30", "벨로스터",
    "맥스크루즈", "베뉴", "아이오닉", "i40", "베라크루즈", "넥쏘", "쏠라티", "아슬란", "아이오닉6"],
    grades: {
      그랜저: [
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
  아반떼: [
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
  쏘나타:[
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
  ],
  싼타페:[
    "싼타페 (MX5) (23년~현재)",
    "더 뉴 싼타페 (20년~23년)",
    "싼타페 TM (18년~20년)",
    "싼타페 더 프라임 (15년~18년)",
    "싼타페 DM (12년~15년)",
    "싼타페 CM (05년~12년)",
    "싼타페 (00년~05년)"
  ],
  스타렉스:[
    "더 뉴 그랜드 스타렉스 (17년~21년)",
    "그랜드 스타렉스 (07년~17년)",
    "스타렉스 점보 (97년~07년)",
    "스타렉스 (97년~07년)"
  ],
  투싼:[
  "더 뉴 투싼 (NX4) (23년~현재)",
  "더 뉴 투싼 하이브리드 (NX4) (23년~현재)",
  "투싼 (NX4) (20년~23년)",
  "투싼 하이브리드 (NX4) (20년~23년)",
  "올 뉴 투싼 (15년~20년)",
  "뉴 투싼 ix (13년~15년)",
  "투싼 ix (09년~13년)",
  "투싼 (04년~09년)"
  ],
  펠리세이드:[
    "더 뉴 펠리세이드(22년~현재)",
    "펠리세이드(18년~22년)"
  ],
  제네시스:[
    "제네시스 DH(13년~16년)",
    "더 뉴 제네시스 쿠페(11년~16년)",
    "제네시스 쿠페(08년~11년)",
    "제네시스(08년~13년)"
  ],
  코나:[
  "코나 일렉트릭 (SX2) (23년~현재)",
  "코나 (SX2) (23년~현재)",
  "코나 하이브리드 (SX2) (23년~현재)",
  "더 뉴 코나 (20년~23년)",
  "더 뉴 코나 하이브리드 (20년~23년)",
  "코나 하이브리드 (19년~20년)",
  "코나 일렉트릭 (18년~23년)",
  "코나 (17년~20년)"
  ],
  에쿠스:[
    "에쿠스(신형)(09년~15년)",
    "에쿠스(99년~09년)"
  ],
  스타리아:[
    "스타리아(21년~현재)"
  ],
  캐스퍼:[
    "캐스퍼(21년~현재)"
  ],
  아이오닉5:[
    "더 뉴 아이오닉5(24년~현재)",
    "아이오닉5(21년~24년)"
  ],
  엑센트:[
    "엑센트(신형)(10년~19년)",
    "뉴 엑센트(97년~99년)",
    "엑센트(94년~97년)"
  ],
  i30:[
    "i30 (PD) (16년~20년)",
    "더 뉴 i30 (15년~16년)",
    "i30(신형) (11년~15년)",
    "i30 cw (08년~11년)",
    "i30 (07년~11년)"
  ],
  벨로스터:[
    "벨로스터 (JS) (18년~22년)",
    "더 뉴 벨로스터 (15년~18년)",
    "벨로스터 (11년~14년)"
  ],
  맥스크루즈:[
    "더 뉴 맥스크루즈(15년~19년)",
    "맥스크루즈(13년~15년)"
  ],
  베뉴:[
    "베뉴(19년~현재)"
  ],
  아이오닉:[
    "더 뉴 아이오닉 일렉트릭(19년~21년)",
    "더 뉴 아이오닉 하이브리드(19년~21년)",
    "아이오닉 일렉트릭(16년~19년)",
    "아이오닉 하이브리드(16년~19년)"
  ],
  i40:[
    "더 뉴 i40 (15년~19년)",
    "더 뉴 i40 살룬 (15년~19년)",
    "i40 살룬 (12년~15년)",
    "i40 (11년~15년)"
  ],
  베라크루즈:[
    "베라크루즈(06년~15년)"
  ],
  넥쏘:[
    "넥쏘(18년~현재)"
  ],
  쏠라티:[
    "쏠라티(20년~현재)"
  ],
  아슬란:[
    "아슬란(14년~18년)"
  ],
  아이오닉6:[
    "아이오닉6(22년~현재)"
  ]
    }
  },
  기아: {
    models: ["카니발","쏘렌토","K5","모닝","레이","K7","스포티지","K3","K8","모하비","셀토스","K9","니로","쏘울","스팅어","EV6","프라이드","포르테","스토닉","카렌스","오피러스","로체","EV9","EV3","엔터프라이즈"],
    grades: {
      카니발: [
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

  K3: [
    "더 뉴 K3 2세대 (21년~현재)",
    "올 뉴 K3 (18년~21년)",
    "더 뉴 K3 쿱 (16년~17년)",
    "더 뉴 K3 유로 (16년~18년)",
    "더 뉴 K3 (15년~18년)",
    "K3 유로 (13년~16년)",
    "K3 쿱 (13년~16년)",
    "K3 (12년~15년)"
  ],

  K5: [
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

  K7: [
    "K7 프리미어 (19년~21년)",
    "K7 프리미어 하이브리드 (19년~21년)",
    "올 뉴 K7 하이브리드 (16년~19년)",
    "올 뉴 K7 (16년~19년)",
    "K7 하이브리드 (13년~16년)",
    "더 뉴 K7 (12년~16년)",
    "더 프레스티지 K7 (11년~12년)",
    "K7 (09년~11년)"
  ],

  K8: [
    "K8 (21년~현재)",
    "K8 하이브리드 (21년~현재)"
  ],

  K9: [
    "더 뉴 K9 2세대 (21년~현재)",
    "더 K9 (18년~21년)",
    "더 뉴 K9 (14년~18년)",
    "K9 (12년~14년)"
  ],

  EV3: [
    "EV3 (24년~현재)"
  ],

  EV6: [
    "더 뉴 EV6 (24년~현재)",
    "EV6 (21년~24년)"
  ],

  EV9: [
    "EV9 (23년~현재)"
  ],

  쏘렌토: [
    "더 뉴 쏘렌토 4세대 (23년~현재)",
    "쏘렌토 4세대 (20년~23년)",
    "더 뉴 쏘렌토 (17년~20년)",
    "올 뉴 쏘렌토 (14년~17년)",
    "뉴 쏘렌토 R (12년~14년)",
    "쏘렌토 R (09년~12년)",
    "뉴쏘렌토 (06년~09년)",
    "쏘렌토 (02년~06년)"
  ],

  모닝: [
    "더 뉴 모닝 (JA) (23년~현재)",
    "모닝 어반 (JA) (20년~23년)",
    "올 뉴 모닝 (JA) (17년~20년)",
    "더 뉴 모닝 (15년~17년)",
    "올 뉴 모닝 (11년~15년)",
    "뉴모닝 (08년~11년)",
    "모닝 (04년~08년)"
  ],

  레이: [
    "더 뉴 기아 레이 EV (23년~현재)",
    "더 뉴 기아 레이 (22년~현재)",
    "더 뉴 레이 (17년~22년)",
    "레이 (11년~17년)"
  ],

  스포티지: [
    "스포티지 5세대 (21년~현재)",
    "스포티지 5세대 하이브리드 (21년~현재)",
    "스포티지 더 볼드 (18년~21년)",
    "스포티지 4세대 (15년~18년)",
    "더 뉴 스포티지 R (13년~15년)",
    "스포티지 R (10년~13년)",
    "New 스포티지 (04년~10년)",
    "스포티지 (93년~02년)"
  ],

  모하비: [
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

  쏘울: [
    "쏘울 부스터 EV (19년~21년)",
    "쏘울 부스터 (19년~21년)",
    "더 뉴 쏘울 (16년~19년)",
    "쏘울 EV (14년~19년)",
    "올 뉴 쏘울 (13년~16년)",
    "쏘울 (08년~13년)"
  ],

  스팅어: [
    "스팅어 마이스터 (20년~현재)",
    "스팅어 (17년~20년)"
  ],

  프라이드: [
    "더 뉴 프라이드 (15년~17년)",
    "올 뉴 프라이드 (11년~15년)",
    "프라이드(신형) (05년~11년)",
    "프라이드 (87년~00년)"
  ],

  포르테: [
    "포르테 해치백 (10년~13년)",
    "포르테 쿱 (09년~13년)",
    "포르테 (08년~13년)"
  ],

  스토닉: [
    "스토닉 (17년~20년)"
  ],

  카렌스: [
    "더 뉴 카렌스 (16년~18년)",
    "올 뉴 카렌스 (13년~16년)",
    "뉴카렌스 (06년~13년)",
    "카렌스 II (02년~06년)",
    "카렌스 (99년~02년)"
  ],

  오피러스: [
    "오피러스 프리미엄 (09년~11년)",
    "뉴오피러스 (06년~09년)",
    "오피러스 (03년~06년)"
  ],

  로체: [
    "로체 이노베이션 (08년~10년)",
    "로체 어드밴스 (07년~08년)",
    "로체 (05년~07년)"
  ],

  엔터프라이즈: [
    "엔터프라이즈 (97년~02년)"
  ]
    }
  },
  제네시스: {
    models: ["G70", "G80", "G90", "GV70", "GV80", "GV90"],
    grades: {
      G80: [
    "일렉트리파이드 G80 (RG3) (21년~현재)",
    "G80 (RG3) (20년~현재)",
    "G80 (16년~20년)"
  ],

  GV70: [
    "일렉트리파이드 GV70 (22년~현재)",
    "GV70 (21년~현재)"
  ],

  G70: [
    "더 뉴 G70 슈팅브레이크 (22년~현재)",
    "더 뉴 G70 (20년~현재)",
    "G70 (17년~20년)"
  ],

  G90: [
    "G90 (RS4) (21년~현재)",
    "G90 (18년~21년)"
  ],

  GV60: [
    "GV60 (21년~현재)"
  ],

  GV80: [
    "GV80 쿠페 (23년~현재)",
    "GV80 (20년~현재)"
  ],
  EQ900:[
    "EQ900(15년~18년)"
  ]
    }
  },
  '쉐보레(GM대우)': {
    models: ["스파크","말리부","트랙스","크루즈","올란도","트레일블레이저","마티즈","알페온","볼트EV","아쿼녹스","다마스","임팔라","캡티바","콜로라도","아베오","라보","트래버스","라세티","카마로","볼트EUV","타호","토스카","볼트","윈스톰","티코"],
    grades: {
      스파크: [
    "더 뉴 스파크 (18년~23년)",
    "더 넥스트 스파크 (15년~18년)",
    "스파크 EV (13년~16년)",
    "스파크 (11년~15년)"
  ],
  말리부: [
    "더 뉴 말리부 (18년~23년)",
    "올 뉴 말리부 (16년~18년)",
    "말리부 (11년~16년)"
  ],
  트랙스: [
    "트랙스 크로스오버 (23년~현재)",
    "더 뉴 트랙스 (16년~22년)",
    "트랙스 (13년~16년)"
  ],
  크루즈: [
    "올 뉴 크루즈 (17년~18년)",
    "어메이징 뉴 크루즈 (15년~17년)",
    "어메이징 뉴 크루즈5 (15년~17년)",
    "크루즈5 (11년~14년)",
    "크루즈 (11년~14년)"
  ],
  올란도: [
    "올란도 (11년~18년)"
  ],
  트레일블레이저: [
    "더 뉴 트레일블레이저 (23년~현재)",
    "트레일블레이저 (20년~23년)"
  ],
  마티즈: [
    "마티즈 크리에이티브 (09년~11년)",
    "마티즈 클래식 (09년~11년)",
    "All New 마티즈 (05년~09년)",
    "마티즈 II (00년~05년)",
    "마티즈 (98년~00년)"
  ],
  알페온: [
    "알페온 (10년~15년)"
  ],
  볼트EV: [
    "뉴 볼트 EV (21년~23년)",
    "볼트 EV (17년~21년)"
  ],
  아쿼녹스: [
    "더 넥스트 이쿼녹스 (22년~현재)",
    "이쿼녹스 (18년~20년)"
  ],
  다마스: [
    "뉴 다마스 (08년~21년)",
    "다마스 II (03년~07년)",
    "다마스 (91년~03년)"
  ],
  임팔라: [
    "임팔라 (15년~20년)"
  ],
  캡티바: [
    "캡티바 (11년~18년)"
  ],
  콜로라도: [
    "올 뉴 콜로라도 (24년~현재)",
    "리얼 뉴 콜로라도 (20년~24년)",
    "콜로라도 (19년~20년)"
  ],
  아베오: [
    "더 뉴 아베오 세단 (16년~19년)",
    "더 뉴 아베오 해치백 (16년~19년)",
    "아베오 세단 (11년~16년)",
    "아베오 해치백 (11년~16년)"
  ],
  라보: [
    "뉴 라보 (08년~21년)",
    "라보 (91년~06년)"
  ],
  트래버스: [
    "트래버스 (19년~현재)"
  ],
  라세티: [
    "라세티 프리미어 (08년~11년)",
    "라세티 (02년~09년)"
  ],
  카마로: [
    "더 뉴 카마로 (18년~22년)",
    "올 뉴 카마로 (16년~18년)",
    "카마로 (11년~15년)"
  ],
  볼트EUV: [
    "볼트 EUV (21년~23년)"
  ],
  타호: [
    "타호 (22년~현재)"
  ],
  토스카: [
    "토스카 프리미엄6 (08년~11년)",
    "토스카 (06년~08년)"
  ],
  볼트: [
    "볼트(Volt) (16년~19년)"
  ],
  윈스톰: [
    "윈스톰 맥스 (08년~10년)",
    "윈스톰 (06년~10년)"
  ],
  티코: [
    "티코 (91년~01년)"
  ]
    }
  },
  '르노코리아(삼성)': {
    models: ["QM6","SM6","SM5","SM3","XM3","SM7","QM3","QM5","마스터","조에","클리오","캡처","트위지","아르카나"],
    grades: {
      QM6: [
    "더 뉴 QM6 (19년~현재)",
    "QM6 (16년~19년)"
  ],
  SM6: [
    "더 뉴 SM6 (20년~현재)",
    "SM6 (16년~20년)"
  ],
  SM5: [
    "SM5 노바 (15년~19년)",
    "뉴SM5 플래티넘 (12년~15년)",
    "뉴SM5(신형) (10년~12년)",
    "SM5 뉴 임프레션 (07년~10년)",
    "뉴SM5 (05년~07년)",
    "SM5 (98년~05년)"
  ],
  SM3: [
    "SM3 네오 (14년~19년)",
    "SM3 Z.E. (13년~20년)",
    "뉴SM3 (09년~14년)",
    "SM3 뉴 제너레이션 (05년~11년)",
    "SM3 (02년~05년)"
  ],
  XM3: [
    "XM3 (20년~24년)"
  ],
  SM7: [
    "SM7 노바 (14년~19년)",
    "All New SM7 (11년~14년)",
    "SM7 New Art (08년~11년)",
    "SM7 (04년~08년)"
  ],
  QM3: [
    "뉴QM3 (17년~19년)",
    "QM3 (13년~17년)"
  ],
  QM5: [
    "QM5 네오 (14년~16년)",
    "뉴QM5 (11년~14년)",
    "QM5 (07년~11년)"
  ],
  마스터: [
    "마스터 (18년~현재)"
  ],
  조에: [
    "조에 (20년~22년)"
  ],
  클리오: [
    "클리오 (18년~19년)"
  ],
  캡처: [
    "캡처 (20년~21년)"
  ],
  트위지: [
    "트위지 (17년~22년)"
  ],
  아르카나: [
    "아르카나 (24년~현재)"
  ]
    }
  },
  'KG모빌리티(쌍용)': {
    models: ["티볼리","렉스턴","코란도","토레스","체어맨","엑티언","무쏘","카이런","로디우스","이스타나","뉴훼미리","칼리스타"],
    grades: {
      티볼리: [
    "더 뉴 티볼리 (23년~현재)",
    "더 뉴 티볼리 에어 (23년~현재)",
    "베리 뉴 티볼리 (19년~23년)",
    "티볼리 아머 (17년~19년)",
    "티볼리 에어 (16년~23년)",
    "티볼리 (15년~17년)"
  ],
  렉스턴: [
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
  코란도: [
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
  토레스: [
    "더 뉴 토레스 (24년~현재)",
    "토레스 EVX (23년~현재)",
    "토레스 (22년~24년)"
  ],
  체어맨: [
    "뉴체어맨 W (11년~17년)",
    "체어맨 H 뉴 클래식 (11년~14년)",
    "체어맨 W (08년~11년)",
    "체어맨 H (08년~11년)",
    "뉴체어맨 (03년~08년)",
    "체어맨 (97년~03년)"
  ],
  엑티언: [
    "액티언 스포츠 (06년~11년)",
    "액티언 (05년~11년)"
  ],
  무쏘: [
    "무쏘 스포츠 (02년~06년)",
    "뉴무쏘 (98년~04년)",
    "뉴무쏘 밴 (98년~04년)",
    "무쏘 (93년~98년)"
  ],
  카이런: [
    "뉴카이런 (07년~11년)",
    "카이런 (05년~07년)"
  ],
  로디우스: [
    "로디우스 유로 (12년~13년)",
    "뉴로디우스 (07년~12년)",
    "로디우스 (04년~07년)"
  ],
  이스타나: [
    "이스타나 (95년~03년)"
  ],
  뉴훼미리: [
    "뉴훼미리 (94년~97년)"
  ],
  칼리스타: [
    "칼리스타 (92년~94년)"
  ]
    }
  },
  BMW: {
    models: ["5시리즈","3시리즈","7시리즈","그란투리스모(GT)","X6","X5","4시리즈","X3","1시리즈","X7","X4","2시리즈","Z4","X1","M4","M3","M2","iX3","i4","6시리즈","M5","8시리즈","X4M","i3","X2","iX","i8","X3M","X6M","X5M","i7","M6","i5","XM","M8","Z3","1M","iX1","M쿠페/로드스터","Z8"],
    grades: {
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
  ]
    }
  },
  벤츠: {
    models: ["E클래스","S클래스","C클래스","GLC클래스","CLS클래스","GLE클래스","A클래스","CLA클래스","G클래스(G바겐)","GLA클래스","AMG GT","GLB클래스","EQS","EQE","GLS클래스","EQB","EQA","SL클래스","M클래스","SLK클래스","B클래스(MY B)","스프린터","GLK클래스","CLE클래스","SLC클래스","V클래스","CL클래스","EQC","CLK클래스","SEL/SEC","GL클래스","SLS AMG","R클래스","190클래스","SLR"],
    grades: {
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
  ]
    }
  },
  볼보: {
    models: ["XC60","XC90","S90","S60","XC40","V60","V40","V90","S80","C40","XC70","C30","S40","S70","940","V50","C70","EX30","V70","740","760","850","960"],
    grades: {
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
  ]
    }
  },
  아우디: {
    models: ["A6","A7","A4","A8","Q5","A5","Q7","Q8","A3","R8","e-트론","Q3","Q4 e-트론","S7","S8","TT","RS7","S4","S6","SQ5","RS5","Q2","S3","TTS","RSQ8","e-트론 GT","S5","RS e-트론 GT","A1","RS3","SQ8","SQ7","100","80","90","RS4","RS6","TTRS","V8","Q8 e-트론","SQ8 e-트론","올로드 콰트로"],
    grades: {
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
  ]
    }
  },
  테슬라: {
    models: ["모델 3","모델 Y","모델 X","모델 S"],
    grades: {
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
  ]
    }
  },
  포르쉐: {
    models: ["카이엔","파나메라","718","911","마칸","타이칸","박스터","카이맨","928","944","968","카레라 GT"],
    grades: {
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
  ]
    }
  },
  랜드로버: {
    models: ["레인지로버","디스커버리","디스커버리 스포츠","레인지로버 스포츠","레인지로버 이보크","레인지로버 벨라","디펜더","프리랜더"],
    grades: {
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
  ]
    }
  },
  닛산: {
    models: ["리프","알티마","리프","370Z","큐브","맥시마","쥬크","무라노","패스파인더","엑스트레일","로그","스카이라인","캐시카이","350Z","GT-R","마치","휘가로","프론티어","NV","노트","로렐","모코","버사","베르사","블루버드 실피","블루버드","세드릭"],
    grades: {
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
  ]
    }
  },
  링컨: {
    models: ["MKZ","에비에이터","MKS","컨티넨탈","네비게이터","MKX","노틸러스","MKC","코세어","타운카","LS","MKT"],
    grades: {
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
  ]
    }
  },
  포드: {
    models: ["포커스","익스플로러","머스탱","F150"],
    grades: {
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
  ]
    }
  },
  폭스바겐: {
    models: ["티구안","골프","아테온","제타","파사트","CC","투아렉","비틀","폴로","시로코","티록","페이톤","ID.4","EOS","보라","기타","리알타","마이크로버스","벤토","사란","아틀라스","코라도","트랜스포터"],
    grades: {
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
  ]
    }
  },
  미니: {
    models: ["쿠퍼","컨트리맨","클럽맨","쿠퍼 컨버터블","쿠페","페이스맨","로드스터","로버 미니"],
    grades: {
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
  ]
    }
  },
  캐딜락: {
    models: ["에스컬레이드","CT6","CTS","ATS","XT5"],
    grades: {
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
  ]
    }
  },
  토요타: {
    models: ["캠리","프리우스","RAV4","시에나","86","알파드","크라운","FJ 크루져"],
    grades: {
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
  ]
    }
  },
  렉서스: {
    models:["ES","NX","RX","LS","UX","CT200h","IS","GS","RC","RZ","LC","SC","GX","LX"],
    grades: {
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
  ]
    }
  },
  애스턴마틴: {
    models: ["라피드"],
    grades: {
      라피드:[
    "라피드 (10년~현재)"
  ]
    }
  },
  마세라티: {
    models: ["기블리","르반떼","콰트로포르테","그란투리스모"],
    grades: {
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
  ]
    }
  },
  푸조: {
    models: ["3008","2008","508","5008"],
    grades: {
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
  ]
    }
  },
  지프: {
    models: ["랭글러","체로키","레니게이드","글래디에이터","컴패스","커맨더","CJ","패트리어트"],
    grades: {
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
  ]
    }
  },
  혼다: {
    models: ["어코드"],
    grades: {
      어코드: [
    "어코드 11세대 (23년~현재)",
    "어코드 10세대 (18년~23년)",
    "올뉴어코드 (08년~17년)",
    "어코드 (76년~07년)"
  ]
    }
  },
  재규어: {
    models: ["XF","XJ","XE","F-PACE","F-TYPE","E-PACE"],
    grades: {
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
  ]
    }
  },
  인피니티: {
    models: ["Q50","QX60"],
    grades: {
      Q50: [
    "Q50 (14년~현재)"
  ],
  QX60: [
    "QX60 (14년~현재)"
  ]
    }
  }
};

// 제조사 선택 시 호출되는 함수
const onCompanyChange = (company) => {
  car.value.model = '';  // 모델 초기화
  car.value.grade = '';  // 세부 모델 초기화
  if (carData[company]) {
    ModelOptions.value = carData[company].models;
  } else {
    ModelOptions.value = [];
  }
};

// 모델 선택 시 호출되는 함수
const onModelChange = (model) => {
  car.value.grade = '';  // 세부 모델 초기화
  if (carData[car.value.company]?.grades[model]) {
    GradeOptions.value = carData[car.value.company].grades[model];
  } else {
    GradeOptions.value = [];
  }
};

const activeButton = ref(null)

// 제조사 선택 버튼 핸들러
const selectManufacturer = (manufacturer, idx) => {
  car.value.manufacturer = manufacturer;
  activeButton.value = idx
  updateCompanyOptions(manufacturer);
};

const updateCompanyOptions = (manufacturer) => {
  if (manufacturer === '국산') {
    CompanyOptions.value = ['현대', '기아', '제네시스' , '쉐보레(GM대우)', '르노코리아(삼성)', 'KG모빌리티(쌍용)'];
  } else if (manufacturer === '수입') {
    CompanyOptions.value = ['BMW', '벤츠', '볼보','아우디','테슬라','포르쉐','랜드로버','닛산','링컨','포드','폭스바겐','미니','캐딜락','토요타','렉서스','애스턴마틴','마세라티','푸조','지프','혼다','재규어','인피니티','폴스타' ];
  }
}

// 변속기 옵션 리스트
const transmissionOptions = ref([
  '자동', '수동', '반자동'
]);

// 이미지 미리보기 배열
const imagePreviews = ref([]);

// 이미지 추가 핸들러
const onFilesAdded = (files) => {
  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const imageObject = {
        id: Date.now() + Math.random(), // 고유 ID 생성
        url: e.target.result,
        file
      };

      // 미리보기 배열에 추가
      imagePreviews.value.push(imageObject);

      // car.value.img 배열에 파일 추가
      car.value.img.push(imageObject.file);
    };
    reader.readAsDataURL(file);
  });
};

// 이미지 제거 핸들러
const onFileRemoved = (file) => {
  // 미리보기 배열에서 제거
  imagePreviews.value = imagePreviews.value.filter(image => image.file !== file);

  // car.value.img 배열에서도 제거
  car.value.img = car.value.img.filter(imgFile => imgFile !== file);
};

// 모든 이미지 제거 핸들러
const onAllFilesRemoved = () => {
  // 미리보기 배열 초기화
  imagePreviews.value = [];

  // car.value.img 배열 초기화
  car.value.img = [];
};


const insert_product = async (product) => {

    console.log("상품 추가 요청:", product);
  try {
    const response = await fetch(`${process.env.API}products_insert`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(product), // product 객체를 JSON으로 변환해 직접 보냄
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log("상품이 성공적으로 추가되었습니다:", result);
    return result;
  } catch (error) {
    console.error("상품 추가 중 오류 발생:", error);
    throw error;
  }
};

const submitProduct = async () => {
  const formData = new FormData();

  // car 객체의 데이터를 FormData에 추가
  for (let key in car.value) {
    if (Array.isArray(car.value[key])) {
      car.value[key].forEach(item => formData.append(key, item));
    } else {
      formData.append(key, car.value[key]);
    }
  }

  // 이미지 파일을 FormData에 추가
  imagePreviews.value.forEach(image => {
    formData.append('image_files', image.file);
  });

  console.log("상품 추가 요청:", formData);

  // API 요청
  try {
    const response = await fetch(`${process.env.API}products_insert`, {
      method: "POST",
      body: formData  // FormData를 전송
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    console.log("상품이 성공적으로 추가되었습니다:", result);
    return result;
  } catch (error) {
    console.error("상품 추가 중 오류 발생:", error);
    throw error;
  }
};





</script>

<style scoped>
.main-container {
  display: flex;
}

.vehicle-listing-page {
  max-width: 600px;
  margin: 0 auto;
}

.full-width {
  width: 100%;
}

.q-pa-md {
  width: 100%;
}

.q-uploader.column.no-wrap {
  width: 100%;
}
.btn-line{
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.category-btn {
  width: 48%; /* 버튼이 나란히 배치되도록 조정 */
  font-size: 14px;
}

.selected-btn {
  background-color: red;
  color: red;
}
.category-btn.active {
  background-color: red;
  color: #000;
}
.q-btn__content {
    font-size: 17px;
    font-weight: bold;
}
</style>
