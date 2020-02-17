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
          <td :colspan="5">
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
import traceroute from './test.json';

export default {
  // eslint-disable-next-line vue/require-prop-types
  props: ['address'],
  data() {
    return {
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
      ]
    };
  },
  watch: {
    address(value, prev) {
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
};
</script>

<style lang="scss" scoped></style>
