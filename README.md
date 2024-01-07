# <img src="images/Logo-circle.png" alt="prjctVes Logo"  height="30"> prjctVes (Temporarily Offline)
<details>
  <summary>Tech Diagram</summary>
  <img src="images/prjctVes_diagram.png" alt="" height=100%>
</details>
                              
Welcome to the GitHub repository for prjctVes, a Discord bot designed to streamline your stock and CS:GO item tracking experience. With prjctVes, you can effortlessly monitor up to 10 stocks and CS:GO items in your watchlist, gaining valuable insights into their current prices and trends. Additionally, the bot offers a convenient search feature in case you just want to take a quick look. The bot is written in Python using [discord.py](https://pypi.org/project/discord.py/).

More notably, prjctVes incorporates a custom-built REST API, which you can explore in more detail [here](https://github.com/MaiTra10/prjctVes-API).

The inspiration for this project stemmed from my daily routine of manually checking both stock prices and CS:GO item values. I recognized that this was an area for automation and figured why not simplify this process for myself and others by delivering comprehensive data with a single Discord command.

### :thinking: How to Use

*To do either options below you will need a Discord account.<br>if you do not have one, you can create one [here](https://discord.com/register) or take a look<br>at the demos provided.*

**If you would like to invite the bot to your own server** | [Invite](https://discord.com/api/oauth2/authorize?client_id=1121275829448605726&permissions=277294345216&scope=bot)

### :hammer_and_wrench: Functionality and Demos

- <details>
  <summary><b>/help</b> | A command to list all the commands of the bot and how to use them</summary>
  <img src="images/gifs/help.gif" alt=""  height="450">
</details>

- <details>
  <summary><b>/wl_add</b> | Used to add an entry to your watchlist</summary>
  <p>
    <details>
      <summary><b>&emsp;Adding Stock and Duplicate Entry Error</b></summary>
      <img src="images/gifs/wl_add_and_error_stock.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Adding CS:GO Item and Duplicate Entry Error</b></summary>
      <img src="images/gifs/wl_add_and_error_steam.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Errors</b></summary>
        <p>
          <details>
            <summary><b>&emsp;&emsp;Invalid Stock/CS:GO Item</b></summary>
            <img src="images/gifs/wl_add_invalid.gif" alt=""  height="450">
          </details>
          <details>
            <summary><b>&emsp;&emsp;Watchlist Limit Reached</b></summary>
            <img src="images/gifs/wl_add_limit.gif" alt=""  height="450">
          </details>
        </p>
    </details>
  </p>
</details>

- <details>
  <summary><b>/wl_remove</b> | Used to remove an entry from your watchlist</summary>
  <p>
    <details>
      <summary><b>&emsp;Removing Stock/CS:GO Item</b></summary>
      <img src="images/gifs/wl_remove.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Errors</b></summary>
        <p>
          <details>
            <summary><b>&emsp;&emsp;Watchlist is Empty</b></summary>
            <img src="images/gifs/wl_remove_empty.gif" alt=""  height="450">
          </details>
          <details>
            <summary><b>&emsp;&emsp;Index is out of Range</b></summary>
            <img src="images/gifs/wl_remove_index.gif" alt=""  height="450">
          </details>
        </p>
    </details>
  </p>
</details>

- <details>
  <summary><b>/wl</b> | Used to display your watchlists or a specific entry from your watchlist</summary>
  <p>
    <details>
      <summary><b>&emsp;Show Specific Stock/CS:GO Item List</b></summary>
      <img src="images/gifs/wl_both_list.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Show Specific Stock/CS:GO Item Data</b></summary>
      <img src="images/gifs/wl_both.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Errors</b></summary>
        <p>
          <details>
            <summary><b>&emsp;&emsp;Watchlist is Empty</b></summary>
            <img src="images/gifs/wl_empty.gif" alt=""  height="450">
          </details>
          <details>
            <summary><b>&emsp;&emsp;Index is out of Range</b></summary>
            <img src="images/gifs/wl_index_error.gif" alt=""  height="450">
          </details>
          <details>
            <summary><b>&emsp;&emsp;User Entry Error</b></summary>
            <img src="images/gifs/wl_edge_case.gif" alt=""  height="450">
          </details>
        </p>
    </details>
  </p>
</details>

- <details>
  <summary><b>/search</b> | Used to search a stock or CS:GO item</summary>
  <p>
    <details>
      <summary><b>&emsp;Search Stock/CS:GO Item</b></summary>
      <img src="images/gifs/search_both.gif" alt=""  height="450">
    </details>
    <details>
      <summary><b>&emsp;Error</b></summary>
        <p>
          <details>
            <summary><b>&emsp;&emsp;Invalid Stock/CS:GO Item</b></summary>
            <img src="images/gifs/search_invalid.gif" alt=""  height="450">
          </details>
        </p>
    </details>
  </p>
</details>
