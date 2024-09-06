<template>
  <q-layout class="container">
    <header class="web-header-container">
      <div class="web-header">
        <div class="logo_img" @click="goMain">
          <img src="~src/img/logo_big.png" alt="목돈로고" />
        </div>
        <ul class="toolbar-menu">
          <li class="menu-item deposit_title">
            <div class="menu-title" @click="goMenu('국산')">국산</div>
          </li>
          <li class="menu-item">
            <div class="menu-title" @click="goMenu('수입')">수입</div>
          </li>
          <li class="menu-item">
            <div class="menu-title" @click="goMenu('판매')">내차팔기</div>
          </li>
          <li class="menu-item">
            <div class="menu-title">시세</div>
          </li>
          <li class="menu-item">
            <div class="menu-title">My</div>
          </li>

        </ul>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
          class="mobile-block"
        />

      </div>
    </header>

    <!-- <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="mobile-block"
    >
      <q-list>
        <q-item-label header> </q-item-label>

        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer> -->

    <q-page-container>
      <router-view />
    </q-page-container>

    <footer>

      <div class="map-box">

        <div class="map-line">
          <div class="map-title">
            국산
          </div>
          <div class="map-list">
            <ul class="map-ul">
              <li>국산차검색</li>
              <li>TRUST CAR진단차량</li>
              <li>리스렌트 차량</li>
              <li>헛걸음보상차량</li>
              <li>TRUST CAR보증</li>
              <li>TRUST CAR프리미엄진단</li>
            </ul>
          </div>
        </div>

        <div class="map-line">
          <div class="map-title">
            수입
          </div>
          <div class="map-list">
            <ul class="map-ul">
              <li>수입차검색</li>
              <li>TRUST CAR진단차량</li>
              <li>리스렌트 차량</li>
              <li>헛걸음보상차량</li>
              <li>TRUST CAR보증수입차</li>
              <li>브랜드 인증차량</li>
              <li>TRUST CAR프리미엄진단</li>
            </ul>
          </div>
        </div>

        <div class="map-line">
          <div class="map-tex">
            <div class="map-title">
              전기 친환경
            </div>
            <div class="map-list">
              <ul class="map-ul">
                <li>전기 친환경차검색</li>
              </ul>
            </div>
            <div class="map-title">
              화물 특장
            </div>
            <div class="map-list">
              <ul class="map-ul">
                <li>화물 특장 버스검색</li>
              </ul>
            </div>
            <div class="map-title">
              TRUST CAR믿고
            </div>
            <div class="map-list">
              <ul class="map-ul">
                <li>TRUST CAR믿고 차량 검색</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="map-line">
          <div class="map-tex2">
            <div class="map-title">
              이차어때?
            </div>
            <div class="map-title">
              TRUST CAR중고차론
            </div>
            <div class="map-title">
              시세
            </div>
          </div>
        </div>

        <div class="map-line">
          <div class="map-title">
            내차팔기
          </div>
          <div class="map-list">
            <ul class="map-ul">
              <li>직거래 간편등록</li>
              <li>딜러 셀프등록</li>
              <li>비교견적</li>
              <li>진단등록</li>
              <li>법인차 매각</li>
            </ul>
          </div>
        </div>

        <div class="map-line">
          <div class="map-tex">
            <div class="map-title">
              매매지원
            </div>
            <div class="map-list">
              <ul class="map-ul">
                <li>매매지원홈</li>
                <li>차량진단</li>
                <li>대출 보험</li>
              </ul>
            </div>
            <div class="map-title">
              매매 가이드
            </div>
            <div class="map-list">
              <ul class="map-ul">
                <li>구매가이드</li>
                <li>판매가이드</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="map-line">
          <div class="map-title">
            미디어
          </div>
          <div class="map-list">
            <ul class="map-ul">
              <li>미디어홈</li>
              <li>핫팁</li>
              <li>영상</li>
              <li>뉴스</li>
              <li>리뷰</li>
              <li>특집</li>
            </ul>
          </div>
        </div>

        <div class="map-line">
          <div class="map-title">
            고객센터
          </div>
          <div class="map-list">
            <ul class="map-ul">
              <li>고객센터홈</li>
              <li>서비스FAQ</li>
              <li>1:1문의</li>
              <li>공지사항</li>
              <li>이벤트</li>
            </ul>
          </div>
        </div>




      </div>


      <!-- <div class="foot_title">TRUST CAR </div>
      <div class="foot-list">
        <div class="list-box">
          회사소개
        </div>
        <div class="list-box">
          인재채용
        </div>
        <div class="list-box">
          지점안내
        </div>
        <div class="list-box">
          매매지원
        </div>
        <div class="list-box">
          이용약관
        </div>
        <div class="list-box">
          고객센터
        </div>
        <div class="list-box">
          디스플레이 광고
        </div>
        <div class="list-box">
          제휴 문의
        </div>
        <div class="list-box">
          개인정보처리방침
        </div>
        <div class="list-box">
          금융소비자보호
        </div>
        <div class="list-box">
          원격지원서비스
        </div>
      </div>





      <div class="foot_info">
        <div>(주)목돈컴퍼니</div>
        <div>대표이사 : 김선우</div>
        <div>사업자 등록번호 : 800-80-08888</div>
        <div>서울특별시 강남구 자곡로 260 5층</div>
        <div>광고/제휴문의 : rlatjsdn@naver.com</div>
      </div> -->

    </footer>

  </q-layout>
</template>

<script setup>
import { ref } from "vue";
import EssentialLink from "components/EssentialLink.vue";
import { useRouter, useRoute } from "vue-router";

defineOptions({
  name: "MainLayout",
});

const $router = useRouter();

const linksList = [
  {
    title: "Docs",
    caption: "quasar.dev",
    icon: "school",
    link: "https://quasar.dev",
  },
  {
    title: "Github",
    caption: "github.com/quasarframework",
    icon: "code",
    link: "https://github.com/quasarframework",
  },
  {
    title: "Discord Chat Channel",
    caption: "chat.quasar.dev",
    icon: "chat",
    link: "https://chat.quasar.dev",
  },
  {
    title: "Forum",
    caption: "forum.quasar.dev",
    icon: "record_voice_over",
    link: "https://forum.quasar.dev",
  },
  {
    title: "Twitter",
    caption: "@quasarframework",
    icon: "rss_feed",
    link: "https://twitter.quasar.dev",
  },
  {
    title: "Facebook",
    caption: "@QuasarFramework",
    icon: "public",
    link: "https://facebook.quasar.dev",
  },
  {
    title: "Quasar Awesome",
    caption: "Community Quasar projects",
    icon: "favorite",
    link: "https://awesome.quasar.dev",
  },
];

const leftDrawerOpen = ref(false);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}

// ******* web toolbar menu ********** //

const goMenu = (menu) => {
  if (menu == "국산") {
    $router.push({
      path: `/product/ProductList`,
    });
  } else if (menu == "수입") {
    $router.push({
      path: `/product/ProductImportedList`,
    });
  } else if (menu == "판매") {
    $router.push({
      path: `/trade/TradeWrite`,
    });
  }
};

const goMain = () => {
  $router.push({
    path: `/`,
  });
};
</script>
<style lang="scss" scoped>
footer {
  background-color: #f8f8f8;
  color: #333;
  text-align: center;
  padding: 40px 0;
  border-top: 1px solid #e0e0e0;
}

.foot_title {
  font-size: 24px;
  font-weight: bolder;
  letter-spacing: 1px;
  font-family: "Noto Sans KR";
}

.foot_content {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 55px;
  padding: 20px 0;
}

.foot_info {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 10px;
  padding: 35px 0 0 0;
}
.foot-list {
    display: flex;
    justify-content: center;
    gap: 50px;
    padding: 20px 0;
}
.map-box{
  display: flex;
  justify-content: center;
  gap: 20px;
}
.map-tex{
  display: flex;
  flex-direction: column;
}
.map-tex2{
  display: flex;
  flex-direction: column;
  gap: 50px;
}
.map-title {
    font-weight: bold;
    font-size: 14px;
}
.map-list {
    padding-top: 10px;
    padding-bottom: 10px;
}
.map-line {
    text-align: left;
}
.map-ul{
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.map-ul li{
  cursor: pointer;
  font-size: 13px;
  color:#8f8f8f
}
</style>
