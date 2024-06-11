// ID        : {{ id }}
// source    : {{ source }}
// url       : {{ url }}
// start time: {{ start_time }}
// end time  :
#include <bits/stdc++.h>
using namespace std;

#define ll long long
#define endl "\n"
#define dbg(v)                                                                 \
  cerr << "Line(" << __LINE__ << ") > " << #v << " = " << (v) << endl;

void solve() {

}

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  cout.tie(NULL);

  {%- if file_input -%}
  freopen("{{ input_file }}", "r", stdin);
  freopen("{{ output_file }}", "w", stdout);
  {%- endif -%}

  {%- if multi_input -%}
  
  ll n;
  cin >> n;

  while (n) {
    solve();
  }
  {%- else -%}
  solve();
  {%- endif -%}

  return 0;
}
