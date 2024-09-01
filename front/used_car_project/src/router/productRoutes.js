const BaseLayout = () => import("../layouts/MainLayout.vue");

const productRoutes = [
  {
    path: "/product",
    name: "product",
    props: true,
    component: BaseLayout,
    children: [
      {
        path: "ProductList",
        name: "ProductList",
        props: true,
        component: () => import("../pages/product/ProductList.vue"),
      },
      {
        path: "ProductDetail/:id",
        name: "ProductDetail",
        props: true,
        component: () => import("../pages/product/ProductDetail.vue"),
      },
      {
        path: "ProductImportedList",
        name: "ProductImportedList",
        props: true,
        component: () => import("../pages/product/ProductImportedList.vue"),
      }
    ],
  },
];
export default productRoutes;
