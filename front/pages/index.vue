<template>
  <v-layout column justify-center align-center>
    <v-flex xs12 md12>
      <v-form ref="form" v-model="valid" class="form">
        <v-row>
          <v-col md="8">
            <v-text-field
              v-model="address"
              label="Search..."
              value="220.247.159.10"
              @keyup.enter="onSearch"
            ></v-text-field>
          </v-col>
          <v-col md="4">
            <v-select
              v-model="type"
              :items="types"
              label="Type"
              required
              class="select-box"
            ></v-select>
          </v-col>
        </v-row>
        <v-btn @click="onSearch">Search</v-btn>
      </v-form>
      <v-spacer></v-spacer>
      <v-spacer></v-spacer>

      <PingResult v-if="type === 'ping'" :address="search.address"></PingResult>
      <TraceResult
        v-if="type === 'traceroute'"
        :address="search.address"
      ></TraceResult>
    </v-flex>
  </v-layout>
</template>

<script>
import TraceResult from '../components/TraceResult';
import PingResult from '../components/PingResult';

export default {
  components: {
    TraceResult,
    PingResult
  },
  data() {
    return {
      valid: true,
      address: '',
      type: 'ping',
      types: ['ping', 'traceroute'],
      search: {
        address: '',
        type: ''
      }
    };
  },
  methods: {
    onSearch() {
      this.search = { address: this.address, type: this.type };
    }
  }
};
</script>

<style lang="scss" scoped>
.form {
  text-align: center;
  margin-bottom: 12px;

  .row {
    width: 600px;
    margin: 0 auto;
  }

  .select-box {
    width: 200px;
  }
}
</style>
