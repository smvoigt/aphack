<template>
  <div>
    <div v-if="data">
      <v-data-table
        :headers="headers"
        :items="data"
        :single-expand="singleExpand"
        :expanded.sync="expanded"
        item-key="id"
        show-expand
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Result</v-toolbar-title>
            <v-spacer></v-spacer>
            <!-- <v-switch
              v-model="singleExpand"
              label="Single expand"
              class="mt-2"
            ></v-switch> -->
          </v-toolbar>
        </template>
        <template v-slot:expanded-item="">
          <td :colspan="7">
            <v-tabs v-model="currentTab" centered>
              <v-tab href="#tab-table">
                Table
              </v-tab>
              <v-tab href="#tab-chart">
                Chart
              </v-tab>
            </v-tabs>
            <v-tabs-items v-model="currentTab">
              <v-tab-item value="tab-table">
                <v-simple-table>
                  <template v-slot:default>
                    <thead>
                      <tr>
                        <th class="text-left">Hop</th>
                        <th class="text-left">From</th>
                        <th class="text-left">Min</th>
                        <th class="text-left">Max</th>
                        <th class="text-left">Avg</th>
                      </tr>
                    </thead>
                    <tbody>
                      <template v-for="item in expanded[0].result">
                        <tr v-if="item.from" :key="item.id">
                          <td>{{ item.hop }}</td>
                          <td>{{ item.from }}</td>
                          <td>{{ item.rtt.min }}</td>
                          <td>{{ item.rtt.max }}</td>
                          <td>{{ item.rtt.avg }}</td>
                        </tr>
                      </template>
                    </tbody>
                  </template>
                </v-simple-table>
              </v-tab-item>
              <v-tab-item value="tab-chart">
                <GChart
                  v-if="expanded[0]"
                  :settings="{ packages: ['corechart', 'timeline'] }"
                  type="Timeline"
                  :data="parseChartData(expanded[0].result)"
                  :options="options"
                />
              </v-tab-item>
            </v-tabs-items>
          </td>
        </template>
      </v-data-table>
    </div>
    <div v-if="loading">
      <v-text-field color="success" loading disabled></v-text-field>
    </div>
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts';
import traceroute from './test.json';

export default {
  components: {
    GChart
  },
  // eslint-disable-next-line vue/require-prop-types
  props: ['address'],
  data() {
    return {
      currentTab: 'tab-table',
      loading: false,
      data: null,
      expanded: [],
      singleExpand: true,
      headers: [
        {
          text: 'Destination name',
          sortable: true,
          value: 'destination_name'
        },
        { text: 'Destination address', value: 'destination_address' },
        { text: 'From', value: 'from' },
        { text: 'Min', value: 'rtt.min' },
        { text: 'Max', value: 'rtt.max' },
        { text: 'Average', value: 'rtt.avg' },
        { text: '', value: 'data-table-expand' }
      ],
      options: {
        height: 700
      }
    };
  },

  watch: {
    address: {
      immediate: true,
      handler(value, prev) {
        if (value !== prev) {
          this.loading = true;
          setTimeout(() => {
            this.data = traceroute.map((i, idx) => {
              let localMin = 9999999;
              let localMax = 0;
              let localTotal = 0;
              let localCount = 0;
              const result = i.result.map((hop, index) => {
                let min = 9999999;
                let max = 0;
                let rttCount = 0;
                let rttTotal = 0;
                let from = '';
                hop.result.forEach((r) => {
                  if (r.rtt) {
                    from = r.from;
                    if (r.rtt > max) {
                      max = r.rtt;
                    }
                    if (r.rtt < min) {
                      min = r.rtt;
                    }
                    rttTotal += r.rtt;
                    rttCount++;
                  }
                });
                let avg;
                if (rttTotal && rttCount) {
                  avg = rttTotal / rttCount;
                  // calculate local min and max
                  if (max > localMax) {
                    localMax = max;
                  }
                  if (min < localMin) {
                    localMin = min;
                  }
                  localTotal += avg;
                  localCount++;
                }

                return {
                  hop: hop.hop,
                  from,
                  rtt: {
                    min: +min.toFixed(2),
                    max: +max.toFixed(2),
                    avg: avg ? +avg.toFixed(2) : 'NaN'
                  },
                  id: index
                };
              });
              const localAvg = localTotal / localCount;

              return {
                id: idx,
                destination_address: i.dst_addr,
                destination_name: i.dst_name,
                from: i.from,
                rtt: {
                  min: +localMin.toFixed(2),
                  max: +localMax.toFixed(2),
                  avg: +localAvg.toFixed(2)
                },
                result
              };
            });
            this.loading = false;
          }, 1000);
        }
      }
    }
  },
  methods: {
    parseChartData(rawData) {
      const data = [['hop', 'label', 'min', 'max']];
      rawData.forEach((i) => {
        const { rtt } = i;
        if (rtt.min < rtt.max) {
          data.push(['' + i.hop, i.from, rtt.min, rtt.max]);
        }
      });
      return data;
    }
  }
};
</script>

<style lang="scss" scoped>
.v-data-table__expanded.v-data-table__expanded__content {
  td {
    padding: 0;
    border: 10px solid grey;
  }
}
</style>
