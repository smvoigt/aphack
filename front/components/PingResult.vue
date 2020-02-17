<template>
  <div>
    <div v-if="data">
      <v-data-table
        :headers="headers"
        :items="data"
        item-key="id"
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
                    <th
                      class="text-left"
                      v-for="header in headers"
                      :key="header.text"
                    >
                      {{ header.text }}
                    </th>
                  </tr>
                </thead>
                <template v-for="item in data">
                  <tr v-if="item.from" :key="item.id">
                    <td>{{ item.destination_address }}</td>
                    <td>{{ item.destination_name }}</td>
                    <td>{{ item.from }}</td>
                    <td>{{ item.min }}</td>
                    <td>{{ item.max }}</td>
                    <td>{{ item.avg }}</td>
                  </tr>
                </template>
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
import ping from './ping.json';

export default {
  // eslint-disable-next-line vue/require-prop-types
  props: ['address'],
  data() {
    return {
      loading: false,
      data: null,
      headers: [
        {
          text: 'Destination name',
          sortable: true,
          value: 'destination_name'
        },
        { text: 'Destination address', value: 'destination_address' },
        { text: 'From', value: 'from' },
        { text: 'Min', value: 'min' },
        { text: 'Max', value: 'max' },
        { text: 'Average', value: 'avg' }
      ]
    };
  },
  watch: {
    address(value, prev) {
      if (value !== prev) {
        this.loading = true;
        setTimeout(() => {
          this.data = ping.map((i, idx) => {
            return {
              id: idx,
              destination_address: i.dst_addr,
              destination_name: i.dst_name,
              from: i.from,
              min: +i.min.toFixed(2),
              max: +i.max.toFixed(2),
              avg: +i.avg.toFixed(2)
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
