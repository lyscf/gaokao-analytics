(() =>
{

mdui.$.extend({
    doms: {
        AJAXProgress: mdui.$('.mdui-progress#global-ajax-progress'),
        announceContent: mdui.$('div.mdui-typo#announce-content'),
        searchKeyword: mdui.$('input.mdui-textfield-input#searck-keyword-input'),
        searchKeywordType: mdui.$('form#search-keyword-type'),
        searchBtn: mdui.$('button#search-start-button'),
        searchResultContainer: mdui.$('section#search-result-container')
    },
    createTable: createTable,
    createActions: createActions
});

window.addEventListener('DOMContentLoaded', () =>
{
    mdui.$.doms.searchBtn.on('click', () =>
    {
        mdui.$.api.search(mdui.$.doms.searchKeyword.val());
    });
    mdui.$.doms.searchKeyword.on('keydown', (e) =>
    {
        if (e.key === 'Enter') mdui.$.api.search(mdui.$.doms.searchKeyword.val());
    });

    mdui.$.api.getAnnounce();
});

function createTable(data, head = [], needContainer = true)
{
    const DOM = {
        TableContainer: document.createElement('div'),
        Table: document.createElement('table'),
        TableHead: document.createElement('thead'),
        TableBody: document.createElement('tbody'),
    };
    const tableHead = [ ...head ];

    if (tableHead.length <= 0)
    {
        for (const name in data[0])
        {
            tableHead.push(name);
        }
    }
    DOM.TableHead.appendChild(createTR(tableHead, null, 'th'));

    for (const _data of data)
    {
        DOM.TableBody.appendChild(createTR(_data, tableHead));
    }

    DOM.Table.appendChild(DOM.TableHead);
    DOM.Table.appendChild(DOM.TableBody);
    DOM.Table.className = 'mdui-table mdui-table-hoverable';

    DOM.TableContainer.appendChild(DOM.Table);
    DOM.TableContainer.className = 'mdui-table-fluid';

    if (needContainer) return DOM.TableContainer;
    else return DOM.Table;

    function createTR(data, head = null, type = 'td')
    {
        const TR = document.createElement('tr');
        const TagName = type === 'th' ? 'th' : 'td';

        if (head)
        {
            for (const _head of head)
            {
                if (data[_head] === null || data[_head] === undefined || data[_head] === '')
                {
                    TR.appendChild(createChild(TagName, '<span class="mdui-text-color-theme-disabled">暂无数据</span>'));
                    continue;
                }
                TR.appendChild(createChild(TagName, data[_head]));
            }
        }
        else
        {
            for (const _data of data)
            {
                TR.appendChild(createChild(TagName, _data));
            }
        }
        

        return TR;

        function createChild(tag, inner)
        {
            const child = document.createElement(tag);
            child.setAttribute('nowrap', 'nowrap');
            if (inner instanceof HTMLElement) child.appendChild(inner);
            else child.innerHTML = inner;
            return child;
        }
    }
}

function createActions(actions)
{
    const ContainerDOM = document.createElement('span');

    for (const action of actions)
    {
        let actionDOM = document.createElement('a');
        let spaceDOM = document.createTextNode('  ');
        if (action.inner instanceof HTMLElement) actionDOM.appendChild(action.inner);
        else actionDOM.innerHTML = action.inner;
        actionDOM.href = 'javascript:' + action.action + ';';
        ContainerDOM.appendChild(actionDOM);
        ContainerDOM.appendChild(spaceDOM);
    }

    ContainerDOM.className = 'mdui-typo';
    return ContainerDOM;
}

})();