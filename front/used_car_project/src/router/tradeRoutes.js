const BaseLayout = () => import("../layouts/MainLayout.vue");

const tradeRoutes = [
  {
    path: "/trade",
    name: "trade",
    props: true,
    component: BaseLayout,
    children: [
      {
        path: "TradeWrite",
        name: "TradeWrite",
        props: true,
        component: () => import("../pages/trade/TradeWrite.vue"),
      }
    ],
  },
];
export default tradeRoutes;
