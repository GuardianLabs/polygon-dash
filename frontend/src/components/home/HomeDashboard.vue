<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import IconCopy from '@/assets/icons/icon-copy.svg';
import { VIOLATIONS_MAP } from '@/utils/violations-map';
import useCopyToClipboard from '@/use/useCopyToClipboard';
import { useRequest } from '@/use/useRequest';
import { fetchTable } from '@/api/api-client';
import { store } from '@/store';

const ORDER_MAP = {
  ascending: 'asc',
  descending: 'desc',
};

const router = useRouter();
const { copyToClipboard } = useCopyToClipboard();
const { sendRequest: getTable, isLoading, data, error } = useRequest(fetchTable);

const violationsMap = Object.fromEntries(VIOLATIONS_MAP);

const tableData = ref([]);
const totalTableEntriesCount = ref(1000);
const tableState = reactive({
  currentPage: 1,
  pageSize: 10,
});
const tableSort = ref({});
let timeoutId = null;

const updateTableState = async (value, key) => {
  tableState[key] = value;
  await fetchTableData();
};

const updateTableSort = async ({ prop, order }) => {
  if (!order) {
    tableSort.value = {};
    await fetchTableData();
    return;
  }
  tableSort.value.order_by = prop;
  tableSort.value.sort_order = ORDER_MAP[order];
  await fetchTableData();
};

const checkIfCurrentPagePossible = computed(() => {
  return tableState.currentPage <= Math.ceil(totalTableEntriesCount.value / tableState.pageSize);
});

const fetchTableData = async () => {
  if (isLoading.value || !checkIfCurrentPagePossible.value) {
    return;
  }
  clearTimeout(timeoutId);
  await getTable([{
    page: tableState.currentPage,
    pagesize: tableState.pageSize,
    ...tableSort.value,
  }]);
  if (error.value) {
    console.error(error.value);
    return;
  }
  if (data.value) {
    totalTableEntriesCount.value = data.value.total;
    tableData.value = [...data.value.data];
  }
  setTimeoutForFetchTableData();
};

const setTimeoutForFetchTableData = () => {
  timeoutId = setTimeout(async () => {
    await fetchTableData();
  }, 10 * 1000);
};

const percentToHSL = (percent) => {
  if (percent > 100) {
    percent = 100;
  }
  const hue = (percent / 100) * 120;
  return { 'color': `hsl(${hue}, 100%, 30%)` };
};

const getViolationTooltip = ({ type, last_violation, violation_severity }) => {

  return `${violationsMap[type].description }` +
    `${last_violation ? `\nLast violation: ${new Date(last_violation * 1000)}` : ''}` +
    `${violation_severity ? `\nSeverity: ${violation_severity}` : ''}`;
};
const navigateToMinerPage = ({ address }) => {
  router.push({ name: 'miner', params: { address, blockchain: store.activeBlockchain } });
};

onMounted(async () => {
  await fetchTableData();
});

onUnmounted(() => {
  clearTimeout(timeoutId);
});

watch(() => store.activeBlockchain, async () => {
  await fetchTableData();
});

</script>

<template>
  <section class="home-dashboard">
    <el-table
      :data="tableData"
      v-loading="isLoading"
      class="home-dashboard__table"
      @sort-change="updateTableSort"
      :default-sort="{prop: 'rank', order: 'ascending'}"
    >
      <el-table-column
        prop="rank"
        label="Rank"
        width="90"
        sortable="custom"
      />
      <el-table-column
        label="Trust"
        prop="score"
        width="90"
        sortable="custom"
      >
        <template #default="{ row }">
          <span :style="percentToHSL((row.score * 100).toFixed(2))">
            {{ (row.score * 100).toFixed(2) }}
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="address"
        label="Address"
        width="205"
      >
        <template #default="{ row }">
          <div class="home-dashboard__table-address">
            <a
              @click="navigateToMinerPage(row)"
              class="home-dashboard__table-address-text"
            >
              {{ row.address }}
            </a>
            <IconCopy
              class="home-dashboard__table-address-copy"
              @click.stop="copyToClipboard(row.address)"
            />
          </div>
        </template>
      </el-table-column>
      <el-table-column
        prop="rank"
        label="Violations"
        class-name="home-dashboard__table-violations"
        min-width="120"
      >
        <template #default="{ row }">
          <el-tag
            v-for="(violation, index) in row.violations"
            :key="index + violation.type"
            class="home-dashboard__table-violation"
            :class="{ 'el-tag--warning': violation.type === 'outlier' }"
          >
            <el-tooltip
              effect="dark"
              :content="getViolationTooltip(violation)"
              placement="top"
              class="home-dashboard__table-violation-tooltip"
            >
              <div>
                <component :is="violationsMap[violation.type].icon"/>
                <div class="home-dashboard__table-violation-text">
                  {{ violation.type }}
                </div>
              </div>
            </el-tooltip>
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="blocks_created"
        label="Blocks"
        width="90"
        sortable="custom"
      >
        <template #default="{ row }">
          {{ (row.blocks_created * 100).toFixed(1) }}%
        </template>
      </el-table-column>
      <el-table-column
        prop="name"
        label="Entity name"
        width="180"
      >
        <template #default="{ row }">
          <el-tag class="home-dashboard__table-entity">
            {{ row.name }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-if="tableData.length"
      class="home-dashboard__pagination"
      small
      layout="prev, pager, next, jumper, ->, sizes, total"
      :total="totalTableEntriesCount"
      :page-sizes="[10, 20, 30, 40]"
      v-model:page-size="tableState.pageSize"
      v-model:current-page="tableState.currentPage"
      @size-change="updateTableState($event, 'pageSize')"
      @current-change="updateTableState($event, 'currentPage')"
    />
  </section>
</template>

<style lang="scss">
@import "@/assets/breakpoints.scss";

.home-dashboard {
  padding: 4rem 0;

  .home-dashboard__table {
    border: 1px solid var(--color-border);
    border-radius: 12px;
    --el-table-header-bg-color: var(--color-background-mute);
    --el-table-text-color: var(--color-text);
    --el-table-header-text-color: var(--color-text);
    --el-table-border: 0;

    table {
      font-size: 0.8rem;
    }

    thead {
      .cell {
        font-weight: 600;
      }
    }

    .home-dashboard__table-address {
      display: grid;
      grid-template-columns: auto 1fr;
      align-items: center;

      .home-dashboard__table-address-text {
        white-space: nowrap;
        text-overflow: ellipsis;
        overflow: hidden;
        cursor: pointer;
        text-decoration: underline;
      }

      .home-dashboard__table-address-copy {
        cursor: copy;
        margin-left: 0.2rem;
      }
    }

    .home-dashboard__table-entity {
      color: var(--color-text);
      background: var(--color-background-mute);
      border: 0;
    }

    .home-dashboard__table-violations {
      .cell {
        display: flex;
        flex-flow: row wrap;
        gap: 0.4rem;

        .el-tag {
          --el-tag-text-color: var(--color-text-danger);
          --el-tag-bg-color: var(--color-background-danger);
          border: 0;
        }

        .el-tag--warning {
          --el-tag-text-color:var(--color-text-warning);
          --el-tag-bg-color: var(--color-background-warning);
          border: 0;
        }
      }
    }

    .home-dashboard__table-violation {
      padding: 0.3rem 0.3rem;
      font-weight: 500;
      cursor: help;

      .home-dashboard__table-violation-text {
        display: none;
      }

      @media screen and (min-width: $breakpoint-desktop) {
        .home-dashboard__table-violation-text {
          display: inline-block;
          height: 100%;
        }
      }

      & > .el-tag__content {
        & > .el-tooltip__trigger {
          display: flex;
          align-items: center;
          gap: 0.2rem;
        }
      }
    }
  }

  .home-dashboard__pagination {
    margin-top: 1rem;
    flex-wrap: wrap;
    gap: 0.5rem 0;
  }
}
</style>
