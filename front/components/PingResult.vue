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
          <td :colspan="7">
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
                    <td>{{ item.destination_city }}</td>
                    <td>{{ item.from_address }}</td>
                    <td>{{ item.from_city }}</td>
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
export default {
  // eslint-disable-next-line vue/require-prop-types
  props: ['address'],
  data() {
    return {
      loading: false,
      data: null,
      headers: [
        { text: 'Destination address', value: 'destination_address' },
        { text: 'Destination city', value: 'destination_city' },
        { text: 'From address', value: 'from_address' },
        { text: 'From city', value: 'from_city' },
        { text: 'Min', value: 'min' },
        { text: 'Max', value: 'max' },
        { text: 'Average', value: 'avg' }
      ]
    };
  },
  watch: {
    address: {
      immediate: true,
      handler(value, prev) {
        if (value && value !== prev) {
          this.loading = true;
          this.data = null;
          this.$axios
            .$get(`${process.env.API}/pingresult?dest=${value}`)
            .then((res) => {
              this.data = res.map((i, idx) => {
                return {
                  id: idx,
                  destination_address: i.dst_addr.address,
                  destination_city: `${i.dst_addr.city} - ${i.dst_addr.country}`,
                  from_address: i.from.address,
                  from_city: `${i.from.city} - ${i.from.country}`,
                  min: +i.min.toFixed(2),
                  max: +i.max.toFixed(2),
                  avg: +i.avg.toFixed(2)
                };
              });
              this.loading = false;
            })
            .catch((e) => {
              this.loading = false;
            });
        }
      }
    }
  }
};
</script>

<style lang="scss" scoped></style>
